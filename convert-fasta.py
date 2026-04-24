if __name__ == '__main__':
    import os
    from pathlib import Path

    base_dir = os.path.dirname(os.path.abspath(__file__))
    seqs_folder = Path(os.path.join(base_dir, os.path.join("protein-engineering", "seqs")))

    for fa_path in seqs_folder.glob("*.fa"):
        with open(fa_path, 'r') as fa_file:
            print(f"Reading in \"{fa_path.absolute()}\"")
            fa_lines = fa_file.readlines()

        if not fa_lines[0].startswith(">"):
            raise ValueError("Cannot pull file name. '>'.")

        filename_base = fa_lines[0].split(",", 1)[0]
        if filename_base.startswith(">RF"):
            filename_base = filename_base[3:]
        else:
            filename_base = filename_base[1:]

        # Original PDB strings
        right_protein_string = "/".join(fa_lines[1].split("/")[:3])

        protein_list = list()
        temp_list = list()
        if len(fa_lines[2:]) % 2 != 0:
            raise ValueError("Uneven file size length.")

        for line in fa_lines[2:]:
            if line.startswith(">"):
                temp_list.append(line)
                continue
            else:
                temp_list.append(line)
                protein_list.append(temp_list)
                temp_list = list()
                continue

        for itr, fa_line in enumerate(protein_list, 1):
            fa_out_name = f"{filename_base}_{itr}"
            fa_out_lines = list()
            temp_headers = fa_line[0][1:].split(",")
            fa_headers = list()
            # Isolate key information (temperature, sample number, score)
            for tmp in temp_headers:
                tmp = tmp.strip()
                if any(tmp.startswith(x) for x in ('T', 'sample', 'score')):
                    fa_headers.append(tmp)

            # Write the header line
            fa_out_lines.append(f">{fa_out_name} | {' | '.join(fa_headers)}\n")

            # Rearranging the sequences for output
            original_parts = fa_lines[1].strip().split("/")
            generated_parts = fa_line[1].strip().split("/")

            # Assume chain labels A, B, C, ...
            chain_order = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")[:len(original_parts)]

            # Find longest generated segment = "novel"
            novel_idx = max(range(len(generated_parts)), key=lambda i: len(generated_parts[i]))

            novel_chain = chain_order[novel_idx]

            # Novel first, then remaining chains in original order
            final_parts = [generated_parts[novel_idx]] + [
                original_parts[i]
                for i in range(len(original_parts))
                if i != novel_idx
            ]

            fa_out_lines.append(f"{'/'.join(final_parts)}\n")

            with open(os.path.join(seqs_folder.absolute(), f"{fa_out_name}.fasta"), 'w') as fa_out:
                output_path = os.path.join(seqs_folder.absolute(), f"{fa_out_name}.fasta")
                print(f'Writing out "{output_path}"...')
                fa_out.writelines(fa_out_lines)

    print(".fa file successfully converted to .fasta files!")