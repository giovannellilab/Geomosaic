import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml


def gather_mifaser(config_file, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mifaser"

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    samples = config["SAMPLES"]

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_mifaser(geomosaic_wdir, samples, output_folder, pivot="ec_number")


def compose_matrix_mifaser(folder, samples, output_folder, pivot):
    unique_list = set()
    list_dfs = []

    for s in samples:
        folder_data = f"{folder}/{s}/mifaser"
        
        flag = True
        if "analysis.tsv" not in listdir(folder_data):
            flag = False
            break

        df = pd.read_csv(f"{folder_data}/analysis.tsv", sep="\t", skiprows=1, names=[pivot,s])
        unique_list.update(list(df[pivot].unique()))
        list_dfs.append(df)

    if flag:
        m = pd.DataFrame(sorted(unique_list), columns=[pivot])
        for x in list_dfs:
            temp = pd.merge(m, x, how="left", on=pivot)
            m = temp.copy()
        
        finalm = m.replace(np.nan, 0, regex=True)
        finalm.to_csv(f"{output_folder}/mifaser.tsv", sep="\t", index=False, header=True)
