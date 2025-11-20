import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_funprofiler(all_samples,geomosaic_wdir,output_base_folder,additional_info):
    pckg = "funprofiler"

    samples = get_sample_with_results(pckg, geomosaic_wdir,all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_funprofiler(geomosaic_wdir, output_folder, samples, pckg)


def compose_matrix_funprofiler(folder, output_folder, samples, pckg):
    
    for t in ['ko_profiles','prefetch_out']:

        unique_list = set()
        list_dfs = []
        pivot = 'ko_id'

        for s in samples:
            folder_data = os.path.join(folder,s,pckg)
            flag = True

            if f"{t}.csv" not in listdir(folder_data):
                flag = False
                break

            raw_df = pd.read_csv(os.path.join(folder_data,f"{t}.csv"), sep=",")

            if t == 'prefetch_out':
                raw_df = raw_df.loc[:,["match_name","intersect_bp"]]
                raw_df.rename(columns={"match_name":pivot,"intersect_bp":s}, inplace=True)
                file_name = "raw_counts_intersect_bp"
            elif t == "ko_profiles":
                raw_df = raw_df.loc[:,[pivot,"abundance"]]
                raw_df.rename(columns={"abundance":s}, inplace=True)
                file_name = t

            raw_df[pivot] = raw_df[pivot].str.replace(r'^ko:','', regex =True)
            unique_list.update(list(raw_df[pivot].unique()))
            list_dfs.append(raw_df)

        if not flag:
            continue
        
        m = pd.DataFrame(sorted(unique_list), columns=[pivot])
        for x in list_dfs:
            temp = pd.merge(m, x, how="left", on=pivot)
            m = temp.copy()
    
        finalm = m.replace(np.nan, 0, regex=True)
        finalm.to_csv(os.path.join(output_folder,f"{file_name}.tsv"), sep="\t", index=False, header=True)
