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


## WSL Environment Setup Guide
This repository provides a step-by-step guide to installing and setting up a Windows Subsystem for Linux (WSL) environment on your Windows machine. WSL allows you to run a Linux distribution alongside your Windows OS, enabling a powerful development environment with access to Linux tools and utilities.

### Table of Contents

Prerequisites  
Step 1: Enable WSL  
Step 2: Install a Linux Distribution  
Step 3: Set Up Your Linux Environment  
Step 4: Update and Upgrade Packages  
Step 5: Optional - Install Additional Tools  
Troubleshooting  
Resources


### Prerequisites

Windows 10 version 2004 and higher (Build 19041 and higher) or Windows 11  
Administrative privileges on your Windows machine  
Internet connection


### Step 1: Enable WSL

Open PowerShell as Administrator.  

Run the following command to enable the WSL feature and the Virtual Machine Platform:
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart


Restart your computer to apply the changes.  

(Optional but recommended) Set WSL 2 as the default version by running:
wsl --set-default-version 2




### Step 2: Install a Linux Distribution

Open the Microsoft Store.  
Search for your preferred Linux distribution (e.g., Ubuntu, Debian, Kali Linux).  
Click Get or Install to download and install the distribution.

Alternatively, you can install a distribution via PowerShell:
wsl --install -d <DistributionName>

Replace <DistributionName> with the name of the distribution (e.g., Ubuntu).

### Step 3: Set Up Your Linux Environment

Launch the installed Linux distribution from the Start menu or by typing wsl in PowerShell or Command Prompt.  
On first launch, you will be prompted to create a new user account and password for the Linux environment. Follow the prompts to complete setup.


### Step 4: Update and Upgrade Packages
Once inside your Linux shell, update the package lists and upgrade installed packages to ensure you have the latest versions:
sudo apt update && sudo apt upgrade -y


### Step 5: Optional - Install Additional Tools
Depending on your development needs, you may want to install additional tools such as:

Git: sudo apt install git  
Build essentials: sudo apt install build-essential  
Python: sudo apt install python3 python3-pip  
Node.js: Follow instructions from NodeSource


### Troubleshooting

If you encounter issues with WSL version, check your current version with:
wsl -l -v


To upgrade an existing distribution to WSL 2:
wsl --set-version <DistributionName> 2


For detailed troubleshooting, visit the official Microsoft WSL documentation:https://docs.microsoft.com/en-us/windows/wsl/troubleshooting


## Custom Scripts
Here are some basic scripts that we devolped to use for each of the different programs under the Rosetta Commons umbrella.

### RFdiffusion
Access the SE2nv environment in the anaconda navigator and run its terminal

cd RFdiffusion

Let’s make a new directory for this test: mkdir test followed by cd test.
Download in PDB 1XQ8: curl -O https://files.rcsb.org/download/1XQ8.pdb

Leave the test folder by running:

cd ..

Force only the CPU to run (lest you get dreaded dgl errors): set CUDA_VISIBLE_DEVICES=-1

Run the following example prompt: 

python scripts/run_inference.py inference.output_prefix=.\test\output\motif_test inference.num_designs=2 contigmap.contigs="[30-45/A48-53/30-45]" inference.input_pdb=.\test\1XQ8.pdb

With any luck this should prepare your proteins! Your outputs are pushed to test/output. The ones you care about opening in PyMOL or pushing to ProteinMPNN are, for instance, motif_test_0.pdb in the main folder.

### ProteinMPNN
Access the mlfold environment in the anaconda navigator and run its terminal

cd ProteinMPNN

Let’s make a new directory for this test: mkdir test followed by cd test.
Download in PDB 5L33: curl -O https://files.rcsb.org/download/5L33.pdb

Leave the test folder by running:

cd ..

Run the following example prompt: 

python protein_mpnn_run.py --pdb_path test/5L33.pdb --out_folder test/output --num_seq_per_target 5 --sampling_temp "0.1 0.2" --seed 42 --batch_size 1

Many things will say it’s not loaded. That’s expected since you never asked for those modules in our example prompt. If you see something like the following result, congratulations! Your ProteinMPNN is set up!

Number of edges: 48
Training noise level: 0.2A
Generating sequences for: 5L33
10 sequences of length 106 generated in 2.2241 seconds

You can find your output sequence in the \test\output\seq\ folder. It’ll be a .FA file you can open with Notepad/Notepad++.
