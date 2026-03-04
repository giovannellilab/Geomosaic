import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_metal_indexes_rb(all_samples,geomosaic_wdir,output_base_folder,additional_info):
    pckg = "rmi_rpi_indexes"
    sub_folder = os.path.join(pckg,"redox_metabolic_plasticity_indexes")

    samples = get_sample_with_results(pckg, geomosaic_wdir,all_samples)
    
    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_metal_indexes_rb(geomosaic_wdir, output_folder, samples, sub_folder)


def compose_matrix_metal_indexes_rb(folder, output_folder, samples, pckg):
    
    for t in ['metal_indexes','metal_indexes_extended']:

        #unique_list = set()
        list_dfs = []
        pivot = 'sample'

        for s in samples:
            folder_data = os.path.join(folder,s,pckg)
            flag = True

            if f"{t}.tsv" not in listdir(folder_data):
                flag = False
                break

            raw_df = pd.read_csv(os.path.join(folder_data,f"{t}.tsv"), sep="\t")
            list_dfs.append(raw_df)

        if not flag:
            continue

        temp = pd.concat(list_dfs)
    
        finalm = temp.replace(np.nan, 0, regex=True)
        finalm.to_csv(os.path.join(output_folder,f"{t}.tsv"), sep="\t", index=False, header=True)
