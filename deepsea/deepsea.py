from Bio.Align.Applications import MafftCommandline
from Bio import SeqIO
from Bio import AlignIO
from Bio.Align import AlignInfo
from io import StringIO
import numpy as np
import tensorflow as tf
import subprocess
import pandas as pd
import math
import joblib
from collections import Counter
import os

ENCODER = joblib.load("class-encoder/CLASS-ENCODER-COMPLETE.joblib")

def translated(Index,Encoder):
    return Encoder.categories_[0][Index]

def ProteinAligner(fasta_input):
    mafft_cline = MafftCommandline(input="-")
    stdout, stderr = mafft_cline(stdin=fasta_input)
    ProteinAlignment = AlignIO.read(StringIO(stdout), "fasta")
    return ProteinAlignment

def ExtractWeights(model,Seq,conv):
    TensorSeq = tf.convert_to_tensor([" ".join(list(Seq))])
    ModelPred = model.predict(TensorSeq, verbose=0)
    PredCLass = np.argmax(ModelPred)
    SoftmaxWeights = model.layers[-1].get_weights()[0]
    SoftmaxWeightsClass = SoftmaxWeights[:,PredCLass]
    Conv1D = tf.keras.Model(model.input,model.get_layer(conv).output)
    Conv1DWeights = Conv1D.predict(TensorSeq, verbose=0)
    Conv1DWeights = np.squeeze(Conv1DWeights)
    FinalWeights = np.dot(Conv1DWeights,SoftmaxWeightsClass)
    FinalWeights = [(x - min(FinalWeights))/(max(FinalWeights)-min(FinalWeights)) for x in FinalWeights]
    return FinalWeights, PredCLass

def PlotAlnWeights(ProteinAlignment, ExtratedWeigths):
    ProbAligned = []
    for ProteinIndex, Protein in enumerate(ProteinAlignment):
        ModelWeightsIndex = ExtratedWeigths[ProteinIndex]
        Count = 0
        Prob = []
        for AminoAcid in Protein.seq:
            if AminoAcid == "-":
                Prob.append(0)
            else:
                Prob.append(ModelWeightsIndex[Count])
                Count += 1
        ProbAligned.append(Prob)
    return ProbAligned

def CreateFasta(tab, path, name):
    with open(f"{path}/{name}.fasta","w") as file:
        for index, row in tab.iterrows():
            file.write(f">{row['#name']}\n")
            file.write(f"{row['seq']}\n")

def DeletFasta(path, name):
    subprocess.run(["rm",f"{path}/{name}.fasta"])

def RunCDHIT(path, name, threshold = 0.95):
    print("Running CD-HIT")
    subprocess.run([
        "cd-hit",
        "-i",f"{path}/{name}.fasta",
        "-o",f"{path}/{name}.cdhit.fasta",
        "-c",str(threshold),
        "-aL",str(0.9),
        "-aS",str(0.9)
        ])
    print("CD-HIT Finished")

def ParseCDhit(path):
    
    clusters = []
    with open(path, 'r') as file:
        cluster_id = None
        for line in file:
            if line.startswith('>Cluster'):
                cluster_id = int(line.strip().split()[1])
            else:
                parts = line.strip().split()
                seq_id = parts[2][1:].split('...')[0]
                is_reference = '*' in parts
                identity = float(parts[-1][:-1]) if not is_reference else 100.0
                clusters.append({
                    "Cluster": cluster_id,
                    "Protein accession": seq_id.split("|")[0],
                    "Is reference": is_reference,
                    "Identity": identity
                })
    clusters_df = pd.DataFrame(clusters)
    return clusters_df

def FilterClusters(clusters, cluster_id, df):
    df = df.copy()
    ClusterIDList = clusters.loc[clusters.Cluster == cluster_id,'Protein accession'].to_list()
    return df[df["Protein accession"].isin(ClusterIDList)]

def ShannonEntropy(Alignment):    
    def Calculate(column):
        count = Counter(column)
        total = sum(count.values())
        entropy = 0.0
        for value in count.values():
            probability = value / total
            entropy -= probability * math.log2(probability)
        return entropy
    FinalEntropy = []
    for i in range(Alignment.get_alignment_length()):
        collumn = Alignment[:, i]
        Entropy = Calculate(collumn)
        FinalEntropy.append(Entropy)
    return FinalEntropy

def ParseFasta(path):
    ProteinId = []
    ProteinSequences = []
    for record in SeqIO.parse(path, "fasta"):
        ProteinId.append(record.id)
        ProteinSequences.append(record.seq)
    return ProteinId, ProteinSequences
def CreateTensor(ProteinSequences):
    return [" ".join(list(x)) for x in ProteinSequences]

def RunModel(ProteinsTensor, model_path):
    model = tf.keras.models.load_model(model_path)



    ModelPred = model.predict(ProteinsTensor, verbose=0)
    
    
    
    ModelClass = np.argmax(ModelPred, axis = 1)
    ModelClass = [translated(x,ENCODER) for x in ModelClass]
    ModelProbs = np.max(ModelPred, axis = 1)
    return ModelClass, ModelProbs