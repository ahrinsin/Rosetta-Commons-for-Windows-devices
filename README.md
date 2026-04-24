# Protein Engineering for Parkinson’s Disease Using RFdiffusion

## Overview

This project focuses on designing and validating novel synthetic proteins capable of binding to α-synuclein oligomers at the β-sheet interface to progress towards targeted degradation therapies for Parkinson’s disease (PD). The work leverages advanced protein design tools including [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion), [ProteinMPNN](https://github.com/dauparas/ProteinMPNN), and [PyRosetta](https://github.com/RosettaCommons/rosetta) to generate candidate binders and analyze their stability and binding potential.

## Background

Alpha-synuclein (aS) is a brain protein that can misfold and aggregate into Lewy bodies, which are implicated in Parkinson’s disease. Ubiquitinating enzymes normally break down these aggregates, but this process is inhibited in PD. This project aims to design proteins that can bind to aS oligomers and encourage their degradation by recruiting E3 ubiquitin ligases.

## Key Features

- Use of RFdiffusion and ProteinMPNN for protein binder design.
- Validation of binding using AlphaFold and Rosetta modeling.
- Integration with ubiquitination pathways for targeted degradation.
- Stepwise installation and usage guides for reproducibility.


## WSL Environment Setup Guide
This repository provides a step-by-step guide to installing and setting up a Windows Subsystem for Linux (WSL) environment on your Windows machine. WSL allows you to run a Linux distribution alongside your Windows OS, enabling a powerful development environment with access to Linux tools and utilities.

### Table of Contents

Prerequisites  
Step 1: Download WSL  
Step 2: Create a Linux Profile  
Step 3: Download Miniconda  
Step 4: Setup Miniconda with Linux  
Troubleshooting  
Resources


### Prerequisites

Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11  
Administrative privileges on your Windows machine  
Internet connection

Compatable versions are listed in the version.txt file of this repository


### Step 1: Enable WSL
Open PowerShell and run:

wsl -install

### Step 2: Create a Linux Profile
After creating a Linux profile, run the following command to update/install the need packages:

sudo apt update && sudo apt upgrade -y

### Step 3: Download Miniconda
Next you need to download Mini conda for Linux using:

curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

Then run:

bash Miniconda3-latest-Linux-x86_64.sh

And follow the steps within the command prompt.

### Step 4: Finish Setup
Restart the command prompt window and open it with "wsl".

Then proceed through the Anaconda TOS:

conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r

### Troubleshooting

If you encounter issues with WSL version, check your current version with:
wsl -l -v


To upgrade an existing distribution to WSL 2:
wsl --set-version <DistributionName> 2


For detailed troubleshooting, visit the official Microsoft WSL documentation:https://docs.microsoft.com/en-us/windows/wsl/troubleshooting


## Custom Scripts
Below is a basic rundown of opening and running each of the different programs.

### RFdiffusion
Download Git [https://git-scm.com/install/windows] and Python (v3.11) [https://www.python.org/downloads/] if not already installed

Make your RFdiff directory and activate it:

conda create -n rfdiff python=3.11 -y && conda activate rfdiff &&(change to your Python version) conda activate rfdiff

Make a folder for the entire project, 

mkdir Protein Engineering

Clone the RFdiffusion GitHub repo → git clone https://github.com/RosettaCommons/RFdiffusion.git && cd RFdiffusion

Install all of your Python packages:

pip install --upgrade pip setuptools wheel && pip install torch==2.4.0 torchvision==0.19 && pip install dgl -f https://data.dgl.ai/wheels/torch-2.4/cu124/repo.html && pip install hydra-core omegaconf pytorch-lightning einops scipy pandas==2.2.2 opt_einsum pyrsistent torchdata==0.8.0 pydantic numpy

Navigate to your SE3Transformer folder: 

cd env/SE3Transformer

Run the following install: 

pip install --no-cache-dir -r requirements.txt

Install SE3Transformer: 

python setup.py install && cd ../.. && pip install -e .

Installing the models; 

mkdir models && cd models. 

Then; 

curl -LOJ "http://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt" && curl -LOJ "http://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt" && curl -LOJ "http://files.ipd.uw.edu/pub/RFdiffusion/60f09a193fb5e5ccdc4980417708dbab/Complex_Fold_base_ckpt.pt"

Create your directory and within it place your input .pdb file. mkdir protein-engineering

### ProteinMPNN
Create your environment (making sure to leave RFdiffusion). 

Exiting ProteinMPNN: conda deactivate && cd ..

conda create -n proteinmpnn python=3.11 -y && conda activate proteinmpnn

Clone the ProteinMPNN GitHub repo into your mlfold environment: 

git clone https://github.com/dauparas/ProteinMPNN.git && cd ProteinMPNN

Install your Python packages. pip install numpy torch

Prepare your directory and within place the RFdiffusion’s output .pdb file. mkdir protein-engineering

Download the convert-fasta.py script and place it into your ProteinMPNN directory.

### PyRosetta
Create your environment (making sure to leave ProteinMPNN). 

Exiting ProteinMPNN: conda deactivate && cd ..

conda create -n pyrosetta python=3.11 -y && conda activate pyrosetta

Download the following: pip install pyrosetta --find-links https://west.rosettacommons.org/pyrosetta/quarterly/release

Create your PyRosetta folder; mkdir PyRosetta && cd PyRosetta && mkdir outputs

Download the scoring.py script and place it into your PyRosetta directory.

## Example Prompt
```
conda activate rfdiff && cd ProteinEngineering/RFdiffusion

python scripts/run_inference.py \
  inference.output_prefix=protein-engineering/output/RFdesign \
  inference.num_designs=1 \
  contigmap.contigs="[PDB_CHAINS LENGTH]" \
  inference.input_pdb=protein-engineering/YOUR_INPUT_PDB.pdb \

conda deactivate && conda activate proteinmpnn && cd .. && cd ProteinMPNN


→ Copy your PDB files to the protein-engineering folder of ProteinMPNN
→ Ensure your RFdesign is manually indexed when running ProteinMPNN
python protein_mpnn_run.py \
  --pdb_path protein-engineering/RFdesign_0.pdb \
  --out_folder protein-engineering \
  --num_seq_per_target 1 \
  --sampling_temp "0.2 0.25 0.3" \
  --batch_size 1

python convert-fasta.py

conda deactivate && conda activate pyrosetta && cd .. && cd PyRosetta
```

→ This script pulls from PDB structures in your RFdiffusion/protein-engineering/output folder and FASTA sequences from your ProteinMPNN/protein-engineering folder
python scoring.py

## Contributors
Reid Buck
Aidan Hrinsin
