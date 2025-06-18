
![DeepSEA](./images/DeepSEA-logo.png)

# Install
**Install conda to control environments**

**To access complete project data and code click on Zenodo button**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13647157.svg)](https://doi.org/10.5281/zenodo.13647157)

**Linux**

Download installer:
```
wget https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh
```
Install conda:
```
bash Anaconda3-2023.09-0-Linux-x86_64.sh
```
Clone this repository and go to the 'DeepSEA-project' directory:
```
git clone https://github.com/computational-chemical-biology/DeepSEA-project.git
cd DeepSEA-project
```
Install and activate the environment depending on your hardware. The GPU-env installation can take a few minutes since it's necessary to install CUDA dependencies:

GPU environment:
```
conda env create -f environment-gpu.yml 
conda activate deepsea-project
```

Test the installation:
```
python DeepSEA.py run --input test/test.fasta --outname run_test_file
```

```
python DeepSEA.py features --input test/test.aln.fasta --outname feat_test_file
```

If everything is correct, a CSV and a PNG files shall appear.

CPU environment:

For cases in which there is no GPU available, there is an option to use DeepSEA in Google Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tiagocabralborelli/DeepSEA-project/blob/main/DeepSEA.ipynb)

# Usage


## **Antimicrobial resistance proteins annotation**

Use the comand <span style="background-color: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 4px; border: 1px solid #ccc; font-family: monospace;">run</span>  to identify proteins that confer resistant phenotypes. The user must input a protein FASTA file. 

**Considerations on the input data**:

- DeepSEA was originally trained on proteins composed by the 20 canonical amino acids, therefore proteins with ambiguous representations will be removed.

- Some protein-prediction tools represent stop codons with "*". Make sure to clean your data before the annotation step.   


```
python DeepSEA.py run --input /path/to/fasta --outname file_name

Options:
  --input TEXT   Path to input fasta file
  --outname     Output file name
```

## **Identifying important regions in multiple sequence alignment**

The command  <span style="background-color: #f0f0f0; color: #333; padding: 2px 6px; border-radius: 4px; border: 1px solid #ccc; font-family: monospace;">features</span> recives an alignment file in **FASTA** format and highlights important regions of each protein in a heatmap. Since DeepSEA can't modify the alignment, make sure there are no proteins with non-canonical amino acids in it.    

DeepSEA can be employed on multiple sequence alignment analysis to reveal regions of interest. 
```
python DeepSEA.py features --input /path/to/fasta --outname feature_heatmap

Options:
  --input TEXT   Path to input: a multiple sequence alignment in fasta format
  --outname     Output file name
```


