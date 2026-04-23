# Protein Engineering for Parkinson’s Disease Using RFdiffusion

## Overview

This project focuses on designing and validating novel synthetic proteins capable of binding to α-synuclein oligomers at the β-sheet interface to progress towards targeted degradation therapies for Parkinson’s disease (PD). The work leverages advanced protein design tools including [RFdiffusion](https://github.com/RosettaCommons/RFdiffusion), ProteinMPNN, and PyRosetta to generate candidate binders and analyze their stability and binding potential.

## Background

Alpha-synuclein (aS) is a brain protein that can misfold and aggregate into Lewy bodies, which are implicated in Parkinson’s disease. Ubiquitinating enzymes normally break down these aggregates, but this process is inhibited in PD. This project aims to design proteins that can bind to aS oligomers and encourage their degradation by recruiting E3 ubiquitin ligases.

## Key Features

- Use of RFdiffusion and ProteinMPNN for protein binder design.
- Validation of binding using AlphaFold and Rosetta modeling.
- Integration with ubiquitination pathways for targeted degradation.
- Stepwise installation and usage guides for reproducibility.

## Installation Summary

For full installation instructions, see [installation/installation_guide.md](installation/installation_guide.md). The setup includes:

- Windows Subsystem for Linux (WSL) environment setup.
- Installation of RFdiffusion and its dependencies.
- Installation of ProteinMPNN and PyRosetta environments.
- Downloading necessary models and scripts.

## Usage

### Running RFdiffusion

```bash
conda activate rfdiff
cd RFdiffusion
python scripts/run_inference.py \
  inference.output_prefix=protein-engineering/output/RFdesign \
  inference.num_designs=1 \
  contigmap.contigs="[A38-55/0 B38-55/0 90-110]" \
  inference.input_pdb=protein-engineering/2n0a_truncated.pdb \
  +inference.seed=10

###Running ProteinMPNN

```bash
conda deactivate && conda activate proteinmpnn
cd ProteinMPNN
python protein_mpnn_run.py \
  --pdb_path protein-engineering/RFdesign_4.pdb \
  --out_folder protein-engineering \
  --num_seq_per_target 5 \
  --sampling_temp "0.2" \
  --seed 121 \
  --batch_size 5

###Running PyRosetta

```bash
conda deactivate && conda activate pyrosetta
cd PyRosetta
python scoring.py

##Results and Next Steps

Identification of candidate binders targeting α-synuclein β-sheet interfaces.
Analysis of binder stability and ubiquitin ligase recruitment potential.
Future work includes linker design, fusion with E3 recruitment motifs, and wet lab validation.

##References

###RFdiffusion GitHub
###Relevant literature on α-synuclein phosphorylation and ubiquitination (see docs/references.md)

Contributors

Reid Buck
Aidan Hrinsin



---

### installation/installation_guide.md

```markdown
# Installation Guide for Protein Engineering Project

This guide provides detailed instructions for setting up the environment and dependencies required to run RFdiffusion, ProteinMPNN, and PyRosetta for protein design targeting Parkinson’s disease.

---

## 1. Installing Windows Subsystem for Linux (WSL)

1. Open PowerShell as Administrator.
2. Run:
   ```bash
   wsl --install


Create your Linux user account.
Update packages:sudo apt update && sudo apt upgrade -y




2. Installing Miniconda

Download Miniconda for Linux:curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh


Run the installer:bash Miniconda3-latest-Linux-x86_64.sh


Restart your shell:wsl


Accept Anaconda Terms of Service:conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main && conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r




3. Installing RFdiffusion

Download and install Git and Python 3.11 if not already installed.
Create and activate the RFdiffusion environment:conda create -n rfdiff python=3.11 -y
conda activate rfdiff


Clone the RFdiffusion repository:git clone https://github.com/RosettaCommons/RFdiffusion.git
cd RFdiffusion


Install Python packages:pip install --upgrade pip setuptools wheel
pip install torch==2.4.0 torchvision==0.19
pip install dgl -f https://data.dgl.ai/wheels/torch-2.4/cu124/repo.html
pip install hydra-core omegaconf pytorch-lightning einops scipy pandas==2.2.2 opt_einsum pyrsistent torchdata==0.8.0 pydantic numpy


Install SE3Transformer:cd env/SE3Transformer
pip install --no-cache-dir -r requirements.txt
python setup.py install
cd ../..
pip install -e .


Download model weights:mkdir models && cd models
curl -LOJ "http://files.ipd.uw.edu/pub/RFdiffusion/6f5902ac237024bdd0c176cb93063dc4/Base_ckpt.pt"
curl -LOJ "http://files.ipd.uw.edu/pub/RFdiffusion/e29311f6f1bf1af907f9ef9f44b8328b/Complex_base_ckpt.pt"
curl -LOJ "http://files.ipd.uw.edu/pub/RFdiffusion/60f09a193fb5e5ccdc4980417708dbab/Complex_Fold_base_ckpt.pt"




4. Installing ProteinMPNN

Deactivate RFdiffusion environment:conda deactivate


Create and activate ProteinMPNN environment:conda create -n proteinmpnn python=3.11 -y
conda activate proteinmpnn


Clone ProteinMPNN repository:git clone https://github.com/dauparas/ProteinMPNN.git
cd ProteinMPNN


Install dependencies:pip install numpy torch


Download convert-fasta.py script and place it in the ProteinMPNN directory.


5. Installing PyRosetta

Deactivate ProteinMPNN environment:conda deactivate


Create and activate PyRosetta environment:conda create -n pyrosetta python=3.11 -y
conda activate pyrosetta


Install PyRosetta:pip install pyrosetta --find-links https://west.rosettacommons.org/pyrosetta/quarterly/release


Create PyRosetta folders:mkdir PyRosetta && cd PyRosetta && mkdir outputs


Download scoring.py script and place it in the PyRosetta directory.


6. Running the Pipeline
RFdiffusion
conda activate rfdiff
cd RFdiffusion
python scripts/run_inference.py \
  inference.output_prefix=protein-engineering/output/RFdesign \
  inference.num_designs=1 \
  contigmap.contigs="[A38-55/0 B38-55/0 90-110]" \
  inference.input_pdb=protein-engineering/2n0a_truncated.pdb \
  +inference.seed=10

ProteinMPNN
conda deactivate && conda activate proteinmpnn
cd ProteinMPNN
python protein_mpnn_run.py \
  --pdb_path protein-engineering/RFdesign_4.pdb \
  --out_folder protein-engineering \
  --num_seq_per_target 5 \
  --sampling_temp "0.2" \
  --seed 121 \
  --batch_size 5
python convert-fasta.py

PyRosetta
conda deactivate && conda activate pyrosetta
cd PyRosetta
python scoring.py

  inference.num_designs=1 \
  contigmap.contigs="[A38-55/0 B38-55/0 90-110]" \
  inference.input_pdb=protein-engineering/2n0a_truncated.pdb \
  +inference.seed=10
