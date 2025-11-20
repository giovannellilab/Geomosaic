import pandas as pd
import numpy as np
from subprocess import check_call
import os
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_hmms_search(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "hmms_search"

    hmmsearch_outfolder = additional_info["assembly_hmmsearch_output_folder"]

    samples = get_sample_with_results(hmmsearch_outfolder, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_hmmsearch(geomosaic_wdir, hmmsearch_outfolder, output_folder, samples)


def complete_hmmsearch(folder, hmmsearch_outfolder, output_folder, samples):
    DF_NORM, All_samples_df = parse_hmmsearch_results(folder, hmmsearch_outfolder, samples)

    concat = pd.concat(All_samples_df, ignore_index=True)
    concat.to_csv(os.path.join(output_folder,"ALL_SAMPLES_HMM_coverage_table.tsv"), sep="\t", header=True, index=False)

    for n in DF_NORM:
        norm_merged = merge_results_by_norm(DF_NORM, norm_method=n)
        norm_merged.to_csv(os.path.join(output_folder,f"{n}.tsv"), sep="\t", header=True, index=False)


def parse_hmmsearch_results(folder, hmmsearch_outfolder, samples):
    DF_norm = {}

    All_samples_df = []

    for s in samples:
        df = pd.read_csv(os.path.join(folder,s,hmmsearch_outfolder,"HMMs_coverage_table.tsv"), sep="\t")
        All_samples_df.append(df)

        norms = list(df.columns)[15:-1]
        cols = ["HMM_model"] + norms
        filt = df[df["perc_conserved"] >= 50].loc[:, cols].drop_duplicates()

        grp = filt.groupby(by="HMM_model").sum().reset_index()

        for n in norms:
            norm_df = grp.loc[:,["HMM_model", n]]
            
            if n not in DF_norm:
                DF_norm[n] = {}
            
            DF_norm[n][s] = norm_df
    
    return DF_norm, All_samples_df


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
