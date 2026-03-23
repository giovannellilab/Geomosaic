import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_metal_indexes_rb(all_samples,geomosaic_wdir,output_base_folder,additional_info):
    pckg = "rmi_rpi_indexes"
    sub_folder = "redox_metabolic_plasticity_indexes"

    samples = get_sample_with_results(pckg, geomosaic_wdir,all_samples,subfolder=sub_folder)
    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_rmi_rpi_indexes(geomosaic_wdir, output_folder, samples, pckg, sub_folder)


def compose_matrix_rmi_rpi_indexes(folder, output_folder, samples, pckg, subfolder):
    
    for t in ['metal_indexes','metal_indexes_extended']:

        list_dfs = []

        for s in samples:
            folder_data = os.path.join(folder,s,pckg,subfolder)
            flag = True
            
            if f"{t}.tsv" not in listdir(folder_data):
                flag = False
                break
            
            df = pd.read_csv(os.path.join(folder_data,f"{t}.tsv"), sep="\t")
            list_dfs.append(df)
            
        if not flag:
            continue

        finalm = pd.concat(list_dfs)
        finalm.to_csv(os.path.join(output_folder,f"{t}.tsv"), sep="\t", index=False, header=True)
