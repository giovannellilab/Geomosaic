import pandas as pd
import numpy as np
from subprocess import check_call
from os import listdir
import os
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_mags_hmmsearch(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mags_hmmsearch"

    mags_hmmsearch_outfolder = additional_info["mags_hmmsearch_output_folder"]

    samples = get_sample_with_results(mags_hmmsearch_outfolder, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_hmmsearch(geomosaic_wdir, mags_hmmsearch_outfolder, output_folder, samples)


def complete_hmmsearch(folder, mags_hmmsearch_outfolder, base_output_folder, samples):
    for s in samples:
        DF_NORM, All_mags_df = parse_hmmsearch_mags(folder, mags_hmmsearch_outfolder, s)

        output_folder = os.path.join(base_output_folder, s)
        check_call(f"mkdir -p {output_folder}", shell=True)

        concat = pd.concat(All_mags_df, ignore_index=True)
        concat.to_csv(os.path.join(output_folder,"ALL_MAGs_HMM_coverage_table.tsv"), sep="\t", header=True, index=False)

        for n in DF_NORM:
            norm_merged = merge_results_by_norm(DF_NORM, norm_method=n)
            norm_merged.to_csv(f"{output_folder}/{n}.tsv", sep="\t", header=True, index=False)


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


def parse_hmmsearch_mags(folder, mags_hmmsearch_output_folder, s):
    DF_norm = {}
    All_mags_df = []
    
    results_folder = os.path.join(folder,s,mags_hmmsearch_output_folder)
    for m in listdir(results_folder):
        folder_data = os.path.join(results_folder,m)
        if not os.path.isdir(folder_data) or not m.startswith("mag_"):
            continue
    
        if "HMMs_coverage_table.tsv" not in listdir(f"{folder_data}"):
            continue
    
        df = pd.read_csv(os.path.join(folder_data,"HMMs_coverage_table.tsv"), sep="\t")
        All_mags_df.append(df)
        
        c1 = df["perc_conserved"] >= 50
        
        norms = list(df.columns)[15:-1]
        cols = ["HMM_model"] + norms
    
        filt = df[c1].loc[:, cols].drop_duplicates()
    
        grp = filt.groupby(by="HMM_model").sum().reset_index()
    
        for n in norms:
            norm_df = grp.loc[:,["HMM_model", n]]
            
            if n not in DF_norm:
                DF_norm[n] = {}
            
            DF_norm[n][m] = norm_df
    
    return DF_norm, All_mags_df
