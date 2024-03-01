import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml


def gather_kaiju(config_file, geomosaic_wdir, output_base_folder):
    pckg = "kaiju"

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    samples = config["SAMPLES"]

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_kaiju(geomosaic_wdir, output_folder, samples)


def compose_matrix_kaiju(folder, output_folder, samples):
    for t in ["phylum", "class", "order", "family", "genus", "species"]:
        pivot = t
        unique_list = set()
        list_dfs = []

        for s in samples:
            folder_data = f"{folder}/{s}/kaiju"
            
            flag = True
            if f"{t}.tsv" not in listdir(folder_data):
                flag = False
                break

            rawdf = pd.read_csv(f"{folder_data}/{t}.tsv", sep="\t")
            df = rawdf.loc[:, ["taxon_name", "percent"]]
            df.rename(columns={"taxon_name": pivot, "percent": s}, inplace=True)
            
            unique_list.update(list(df[pivot].unique()))
            list_dfs.append(df)

        if not flag:
            continue

        m = pd.DataFrame(sorted(unique_list), columns=[pivot])
        for x in list_dfs:
            temp = pd.merge(m, x, how="left", on=pivot)
            m = temp.copy()
        
        finalm = m.replace(np.nan, 0, regex=True)
        finalm.to_csv(f"{output_folder}/{t}.tsv", sep="\t", index=False, header=True)
