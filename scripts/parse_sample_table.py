
import pandas as pd
from subprocess import check_call


def parse_sample_table(folder_raw_reads, working_dir, sample_table):
    print("Mapping samples to filenames...")

    samples_list = group_read_by_sample(
        filename=sample_table,
        rawreads_folder=folder_raw_reads,
        wdir=working_dir
    )   
    
    return samples_list, working_dir


def group_read_by_sample(filename, rawreads_folder, wdir):
    df = pd.read_csv(filename, sep="\t")

    grp = df.groupby(by="sample").agg(list)
    grp.reset_index(inplace=True)

    samples_list = []

    for i in list(grp.itertuples())[:2]:        
        samples_list.append(i.sample)

        all_r1 = " ".join([f"{rawreads_folder}/{x}" for x in i.r1])
        all_r2 = " ".join([f"{rawreads_folder}/{x}" for x in i.r2])

        # check_call(f"mkdir -p {wdir}/{i.sample}", shell=True)

        # check_call(f"cat {all_r1} > {wdir}/{i.sample}/R1.fastq.gz", shell=True)
        # check_call(f"cat {all_r2} > {wdir}/{i.sample}/R2.fastq.gz", shell=True)
    
    return samples_list
