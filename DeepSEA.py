import click
import os
from deepsea.deepsea import *
from Bio import AlignIO
import seaborn as sns
import matplotlib.pyplot as plt

@click.group()
def deepsea():
    pass

@deepsea.command()
@click.option("--input",  help = "Path to input fasta file")
@click.option("--outname", help = "Output file name")

def run(input, outname, model_path = "./models/cnn-model"):

    ProteinId, ProteinSequences = ParseFasta(input)
    ProteinsTensor = CreateTensor(ProteinSequences)
    ModelClass, ModelProbs = RunModel(ProteinsTensor, model_path)
    
    Results = pd.DataFrame({"Name":ProteinId,"Class":ModelClass,"Prob":ModelProbs})
    Results.to_csv(f"{outname}.tsv", index = False, sep = "\t")


@deepsea.command()
@click.option("--input",  help = "Path to input fasta file")
@click.option("--outname", help = "Output file name")

def features(input, outname):
    Model = tf.keras.models.load_model("./models/cnn-model")
    Alignment = AlignIO.read(input, "fasta")
    ProteinSequences = [record.seq.ungap("-") for record in Alignment]

    ExtratedWeigths, PredictedClasses = [], []
    for Protein in ProteinSequences:
        Weights, Classes = ExtractWeights(Model, Protein, "4_conv")
        ExtratedWeigths.append(Weights)
        PredictedClasses.append(Classes)
    
    FeatureMatrix = PlotAlnWeights(Alignment, ExtratedWeigths)

    plt.figure(figsize=(10,3))
    sns.heatmap(FeatureMatrix, cmap = "coolwarm")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(f"{outname}.png")

if __name__ == '__main__':
    deepsea()