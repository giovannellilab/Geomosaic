import pandas as pd
import numpy as np
from subprocess import check_call
import os
import yaml


def gather_hmms_search(config_file, geomosaic_wdir, output_base_folder):
    pckg = "hmms_search"

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    samples = config["SAMPLES"]

    hmmsearch_outfolder = config["ADDITIONAL_PARAM"]["assembly_hmmsearch_output_folder"]

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_hmmsearch(geomosaic_wdir, hmmsearch_outfolder, output_folder, samples)


def complete_hmmsearch(folder, hmmsearch_outfolder, output_folder, samples):
    DF_NORM = parse_hmmsearch_results(folder, hmmsearch_outfolder, samples)

    for n in DF_NORM:
        norm_merged = merge_results_by_norm(DF_NORM, norm_method=n)
        norm_merged.to_csv(f"{output_folder}/{n}.tsv", sep="\t", header=True, index=False)


def parse_hmmsearch_results(folder, hmmsearch_outfolder, samples):
    DF_norm = {}

    for s in samples:
        df = pd.read_csv(f"{folder}/{s}/{hmmsearch_outfolder}/HMMs_coverage_table.tsv", sep="\t")
        norms = list(df.columns)[15:-1]
        cols = ["HMM_model"] + norms
        filt = df[df["perc_conserved"] >= 70].loc[:, cols].drop_duplicates()

        grp = filt.groupby(by="HMM_model").sum().reset_index()

        for n in norms:
            norm_df = grp.loc[:,["HMM_model", n]]
            
            if n not in DF_norm:
                DF_norm[n] = {}
            
            DF_norm[n][s] = norm_df
    
    return DF_norm


def merge_results_by_norm(DF_NORM, norm_method):
    db_list = []
    for _, x in DF_NORM[norm_method].items():
        db_list += list(x["HMM_model"])
    
    unique_db_list = sorted(set(db_list))
    
    m = pd.DataFrame(unique_db_list, columns=["HMM_model"])
    
    for s, x in DF_NORM[norm_method].items():
        temp_sample_df = x.copy()
        temp_sample_df.rename(columns={norm_method: s}, inplace=True)
        temp = pd.merge(m, temp_sample_df, how="left", on="HMM_model")
        m = temp.copy()
    
    newm = m.fillna(0)
    return newm
