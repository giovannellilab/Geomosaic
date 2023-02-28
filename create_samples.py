#!/usr/bin/env python3
#

import pandas as pd
from subprocess import check_call


def main():
    print("Mapping samples to filenames...")
    file = "data_mapping.tsv"

    rawdf = pd.read_csv(file, sep="\t", names=["filenames", "sample_name"])
    df = rawdf[rawdf["filenames"].str.contains(".fastq.gz")]
    grp = df.groupby(by=["sample_name"]).agg(list)
    grp.reset_index(inplace=True)

    mapping = {}

    for i in grp.itertuples():
        sample = i.sample_name
        file_list = i.filenames

        if sample not in mapping:
            mapping[sample] = {"r1": [], "r2": []}
        
        for f in file_list:
            if "R1" in f:
                mapping[sample]["r1"].append(f)
            else:
                assert "R2" in f
                mapping[sample]["r2"].append(f)

    sorted_mapping = {}
    for sample in mapping:
        r1 = mapping[sample]["r1"]
        r2 = mapping[sample]["r2"]

        sorted_mapping[sample] = {"r1": sorted(r1), "r2": sorted(r2)}

    # Check if R1 and R2 files exists
    print("Checking existing of R1 and R2 files for each sample...")
    for sample in sorted_mapping:
        r1_files = sorted_mapping[sample]["r1"]
        r2_files = sorted_mapping[sample]["r2"]

        for r1, r2 in zip(r1_files, r2_files):
            prefix_r1, suffix_r1 = r1.split("R1")
            prefix_r2, suffix_r2 = r2.split("R2")

            assert prefix_r1 == prefix_r2, f"R1 and R2 files are not matching.\nR1 file: {r1}\nR2 file: {r2}\n"
            assert suffix_r1 == suffix_r2, f"R1 and R2 files are not matching.\nR1 file: {r1}\nR2 file: {r2}\n"
    
    print("Prepairing samples files...")
    # input="raw_metagenomes/somnus"
    wdir_somnus="raw_metagenomes/somnus"
    folder_raw_reads = "raw_metagenomes/GiovanARG19MetaG"

    check_call(f"mkdir -p {wdir_somnus}", shell=True)

    template = list(sorted_mapping.items())
    samples_list = []
    for sample, reads_files in template[:2]:
        assert len(reads_files["r1"]) == len(reads_files["r2"]), f"For this Sample {sample}, there are different number of R1 and R2 files"
        sample_folder = f"{wdir_somnus}/{sample}"
        check_call(f"mkdir -p {sample_folder}", shell=True)
        r1 = " ".join(map(lambda x: f"{folder_raw_reads}/{x}", reads_files["r1"]))
        r2 = " ".join(map(lambda x: f"{folder_raw_reads}/{x}", reads_files["r2"]))
        check_call(f"cat {r1} > {sample_folder}/R1.fastq.gz", shell=True)
        check_call(f"cat {r2} > {sample_folder}/R2.fastq.gz", shell=True)
        samples_list.append(sample)
    
    s = f"""SAMPLES={str(repr(samples_list))}
WDIR={str(repr(wdir_somnus))}

"""

    check_call(f"""printf "{s}" | cat - Snakefile > temp && mv temp Snakefile""", shell=True)
    print("Done.")


if __name__ == "__main__":
    main()
