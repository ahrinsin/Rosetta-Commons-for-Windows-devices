# Rosetta-Commons-changes-for-Windows-devices
Here are the steps we took to convert the scripts used to run RFdiffusion, ProteinMPNN and PyRosetta to be more accessible and easy to run on Windows devices.
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
