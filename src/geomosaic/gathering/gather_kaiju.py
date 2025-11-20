import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_kaiju(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "kaiju"
 
    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_kaiju(geomosaic_wdir, output_folder, samples, pckg)


def compose_matrix_kaiju(folder, output_folder, samples, pckg):
    for t in ["phylum", "class", "order", "family", "genus", "species"]:
        pivot = t
        unique_list = set()
        list_dfs_percent = []
        list_dfs_reads = []

        for s in samples:
            folder_data = os.path.join(folder,s,pckg)
            
            flag = True
            if f"{t}.tsv" not in listdir(folder_data):
                flag = False
                break

            rawdf = pd.read_csv(os.path.join(folder_data,f"{t}.tsv"), sep="\t")
            
            df_percent = rawdf.loc[:, ["taxon_name", "percent"]]
            df_percent.rename(columns={"taxon_name": pivot, "percent": s}, inplace=True)

            df_reads = rawdf.loc[:, ["taxon_name", "reads"]]
            df_reads.rename(columns={"taxon_name": pivot, "reads": s}, inplace=True)
            
            unique_list.update(list(df_percent[pivot].unique()))
            
            list_dfs_percent.append(df_percent)
            list_dfs_reads(df_reads)

        if not flag:
            continue

        m_percent = pd.DataFrame(sorted(unique_list), columns=[pivot])
        m_reads = pd.DataFrame(sorted(unique_list), columns=[pivot])

        for x1 in list_dfs_percent:
            temp_1 = pd.merge(m_percent, x1, how="left", on=pivot)
            m_percent = temp_1.copy()
        for x2 in list_dfs_reads:
            temp_2 = pd.merge(m_reads, x2, how="left", on=pivot)
            m_reads = temp_2.copy()

        finalm_percent = m_percent.replace(np.nan, 0, regex=True)
        finalm_percent.to_csv(os.path.join(output_folder,f"{t}.tsv"), sep="\t", index=False, header=True)

        finalm_reads = m_reads.replace(np.nan, 0, regex=True)
        finalm_reads.to_csv(os.path.join(output_folder,f"{t}_reads.tsv"), sep="\t", index=False, header=True)

