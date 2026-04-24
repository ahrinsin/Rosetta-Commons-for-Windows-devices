import glob
import os
import re
import pyrosetta
from pyrosetta import *
from pyrosetta.rosetta.protocols.simple_moves import SimpleThreadingMover
from pyrosetta.rosetta.protocols.minimization_packing import PackRotamersMover
from pyrosetta.rosetta.protocols.idealize import IdealizeMover
from pyrosetta.rosetta.protocols.relax import FastRelax
from pyrosetta.rosetta.protocols.analysis import InterfaceAnalyzerMover
from pyrosetta.rosetta.core.pack.task import TaskFactory
from pyrosetta.rosetta.core.pack.task.operation import RestrictToRepacking

pyrosetta.init(
    "-ex1 -ex2 -ex1aro -ex2aro "
    "-ignore_unrecognized_res 1 "
    "-load_PDB_components false "
    "-ignore_waters true "
    "-mute all "
    "-mute core.pack core.scoring core.conformation protocols.idealize protocols.relax"
)

print("PyRosetta initialized.")

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

fasta_files = glob.glob("ProteinMPNN/protein-engineering/seqs/*.fasta")
print(f"Found {len(fasta_files)} FASTA files to process.")

score_summary = []

for fasta_path in fasta_files:
    base_name = os.path.splitext(os.path.basename(fasta_path))[0]
    print(f"\n=== Processing {base_name} ===")

    # Match FASTA to its PDB
    match = re.match(r"design_(\d+)_\d+", base_name)
    if not match:
        raise ValueError(f"Unexpected FASTA name format: {base_name}")

    backbone_idx = match.group(1)

    pdb_path = f"RFdiffusion/protein-engineering/output/RFdesign_{backbone_idx}.pdb"

    print(f"Using PDB: {pdb_path} for FASTA: {base_name}")

    if not os.path.exists(pdb_path):
        raise FileNotFoundError(f"PDB not found: {pdb_path}")

    pose = pose_from_pdb(pdb_path)

    # Find binder chain
    binder_chain_info = None
    for i in range(1, pose.num_chains() + 1):
        start = pose.chain_begin(i)
        end = pose.chain_end(i)
        length = end - start + 1
        gly_content = pose.sequence()[start-1:end].count("G") / length if length > 0 else 0
        if gly_content > 0.90:
            binder_chain_info = {"start": start, "end": end, "length": length}
            break

    if not binder_chain_info:
        raise ValueError("Could not find designed binder chain")

    # Read sequence
    with open(fasta_path, "r") as f:
        raw = "".join(line.strip() for line in f if not line.startswith(">"))
    fasta_fragments = [f.strip() for f in raw.split("/") if f.strip()]

    # Always take the longest FASTA fragment as the designed binder
    binder_seq = max(fasta_fragments, key=len)

    # Enforce correct length match to the glycine chain
    if len(binder_seq) != binder_chain_info["length"]:
        raise ValueError(
            f"Longest FASTA fragment length ({len(binder_seq)}) "
            f"does not match binder chain length ({binder_chain_info['length']})"
        )

    # Thread sequence
    print("Threading sequence...")
    full_seq = list(pose.sequence())
    start_idx = binder_chain_info["start"] - 1
    for i, aa in enumerate(binder_seq):
        full_seq[start_idx + i] = aa.upper()

    thread_mover = SimpleThreadingMover()
    thread_mover.set_sequence("".join(full_seq), binder_chain_info["start"])
    thread_mover.apply(pose)

    scorefxn = get_fa_scorefxn()

    # Repack
    print("Repacking sidechains...")
    tf = TaskFactory()
    tf.push_back(RestrictToRepacking())
    pack_mover = PackRotamersMover(scorefxn, tf)
    pack_mover.apply(pose)

    # Idealize + Relax
    print("Idealizing and relaxing...")
    IdealizeMover().apply(pose)
    FastRelax(scorefxn, 3).apply(pose)

    total_score = scorefxn(pose)
    score_per_res = total_score / pose.total_residue()

    # Interface Analysis
    iam = InterfaceAnalyzerMover()
    iam.set_scorefunction(scorefxn)
    iam.set_pack_input(False)
    iam.set_pack_separated(False)
    iam.apply(pose)

    ddG = iam.get_interface_dG()
    dSASA = iam.get_interface_delta_sasa()

    ratio = ddG / dSASA if dSASA > 0 else 0

    print(f"FINAL ROSETTA SCORE : {total_score:.3f}")
    print(f"Score per residue   : {score_per_res:.3f}")
    print(f"Interface ddG       : {ddG:.3f}")
    print(f"Interface dSASA     : {dSASA:.1f} Ų")
    print(f"ddG / dSASA         : {ratio:.6f}")

    # Full Energy Table
    energies = pose.energies()
    emap = energies.total_energies()

    txt_lines = [
        f"Design: {base_name}\n",
        f"Total Rosetta score: {total_score:.3f}\n",
        f"Score per residue: {score_per_res:.3f}\n",
        f"Interface ddG: {ddG:.3f}\n",
        f"Interface dSASA: {dSASA:.1f}\n",
        f"ddG/dSASA: {ratio:.6f}\n\n",
        "Full Energy Breakdown\n",
        f"{'Term':<20} {'Weight':>8} {'Raw':>12} {'Weighted':>12}\n",
        "-" * 55 + "\n"
    ]

    score_types = [
        "fa_atr", "fa_rep", "fa_sol", "fa_intra_rep", "fa_elec",
        "fa_intra_sol_xover4", "lk_ball_wtd", "fa_intra_elec",
        "pro_close", "hbond_sr_bb", "hbond_lr_bb", "hbond_bb_sc",
        "hbond_sc", "dslf_fa13", "omega", "fa_dun", "p_aa_pp",
        "ref", "rama_prepro"
    ]

    for st_name in score_types:
        st = getattr(pyrosetta.rosetta.core.scoring.ScoreType, st_name)
        raw = emap[st]
        weight = scorefxn.get_weight(st)
        weighted = raw * weight
        txt_lines.append(f"{st_name:<20} {weight:8.3f} {raw:12.3f} {weighted:12.3f}\n")

    txt_lines.append("\nResidue   Chain   TotalEnergy\n")
    txt_lines.append("--------------------------------\n")

    for i in range(1, pose.total_residue() + 1):
        res_total = energies.residue_total_energy(i)
        chain_id = pose.pdb_info().chain(i)
        txt_lines.append(f"{i:7d}   {chain_id:5}   {res_total:8.3f}\n")

    # Save files
    os.makedirs("PyRosetta/outputs", exist_ok=True)
    txt_path = f"PyRosetta/outputs/{base_name}.txt"
    pdb_path_out = f"PyRosetta/outputs/{base_name}.pdb"

    with open(txt_path, "w") as f:
        f.writelines(txt_lines)

    pose.dump_pdb(pdb_path_out)
    print(f"Saved: {base_name}.pdb  |  Score = {total_score:.3f}  |  ddG = {ddG:.3f}")

    score_summary.append((base_name, total_score, score_per_res, ddG, dSASA, ratio))

# Summary table
summary_path = "PyRosetta/outputs/all_scores.txt"
with open(summary_path, "w") as f:
    f.write("Design_Name          Rosetta_Score   Score/Res  ddG     dSASA    ddG/dSASA\n")
    f.write("-------------------------------------------------------------------------------\n")
    for item in score_summary:
        f.write(f"{item[0]:<20} {item[1]:12.3f} {item[2]:10.3f} {item[3]:8.3f} {item[4]:8.1f} {item[5]:11.6f}\n")

print(f"\n=== All designs processed! ===")
print(f"Summary saved to: {summary_path}")