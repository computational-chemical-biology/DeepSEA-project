
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
Install and activate environment depending on your hardware. The gpu-env installation can take a few minutes since it's necessary to install CUDA dependencies:

GPU environment:
```
conda env create -f environment-gpu.yml 
conda activate deepsea-project
```
CPU environment:
```
conda env create -f environment-cpu.yml
conda activate deepsea-project-cpu
```

# Usage
Test the installation:
```
python DeepSEA.py run --input test/test.fasta --outname test_file
```
If everything is correct, a CSV file shall appear.

**Command: run**
```
python DeepSEA.py predict --input /path/to/fasta --outname file_name

Options:
  --input TEXT   Path to input fasta file
  --outname     Output file name
```
**Command: features**
```
python DeepSEA.py predict --features /path/to/fasta --outname feature_heatmap

Options:
  --input TEXT   Path to input fasta file
  --outname     Output file name
```