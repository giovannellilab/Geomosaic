import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_mifaser(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mifaser"
    
    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_mifaser(geomosaic_wdir, samples, output_folder, pckg, pivot="ec_number")


def compose_matrix_mifaser(folder, samples, output_folder, pckg, pivot):
    unique_list = set()
    list_dfs = []

    for s in samples:
        folder_data = os.path.join(folder,s,pckg)
        
        flag = True
        if "analysis.tsv" not in listdir(folder_data):
            flag = False
            break

        df = pd.read_csv(os.path.join(folder_data,"analysis.tsv"), sep="\t", skiprows=1, names=[pivot,s])
        unique_list.update(list(df[pivot].unique()))
        list_dfs.append(df)

    if flag:
        m = pd.DataFrame(sorted(unique_list), columns=[pivot])
        for x in list_dfs:
            temp = pd.merge(m, x, how="left", on=pivot)
            m = temp.copy()
        
        finalm = m.replace(np.nan, 0, regex=True)
        finalm.to_csv(os.path.join(folder_data,"mifaser.tsv"), sep="\t", index=False, header=True)
