import pandas as pd
import numpy as np
from subprocess import check_call
from os import listdir
import os
import yaml


def gather_coverm_genome(config_file, geomosaic_wdir, output_base_folder):
    pckg = "coverm_genome"

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    samples = config["SAMPLES"]

    gtdbtk_gather = os.path.join(output_base_folder, "mags_gtdbtk")
    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_coverm_genome(geomosaic_wdir, output_folder, gtdbtk_gather, samples)


def complete_coverm_genome(folder, output_folder, gtdbtk_gather, samples):
    DF_NORM = parse_coverm_genome(folder, gtdbtk_gather, samples)

    for level in ["phylum", "class", "order", "family", "genus", "species"]:
        res = taxa_level_abundances(DF_NORM, level)

        for norm, dfnorm in res.items():
            dfnorm.to_csv(f"{output_folder}/{level}_{norm}.tsv", sep="\t", index=False, header=True)


def taxa_level_abundances(DF_NORM, level):
    assert level in ["phylum", "class", "order", "family", "genus", "species"]

    df = {}
    
    for norm in DF_NORM:
        db_list = []
        for s, x in DF_NORM[norm].items():
            db_list += list(x[level])

        unique_db_list = sorted(set([i if i == i else "unclassified_" for i in db_list]))
            
        m = pd.DataFrame(unique_db_list, columns=[level])
        
        for s, x in DF_NORM[norm].items():
            temp_sample_df = x.loc[:,[level, norm]].groupby(by=level).sum().reset_index()
            temp_sample_df.rename(columns={norm: s}, inplace=True)
            temp = pd.merge(m, temp_sample_df, how="left", on=level)
            m = temp.copy()
        
        newm = m.fillna(0)

        df[norm] = newm
    return df


def parse_coverm_genome(folder, gtdbtk_gather, samples):
    DF_NORM = {}

    for s in samples:
        sample_folder = f"{folder}/{s}/coverm_genome/"
        methods = []
        
        with open(f"{sample_folder}/list.txt") as fd:
            for line in fd:
                methods.append(line.rstrip("\n"))
        
        for mtd in methods:
            if mtd not in DF_NORM:
                DF_NORM[mtd] = {}
        
            df_mtd = pd.read_csv(f"{sample_folder}/{mtd}.tsv", sep="\t")
            df_mtd.columns = ["MAGs", mtd]

            df_mtd = df_mtd[df_mtd["MAGs"] != "unmapped"]

            # GEOMOSAIC GTDBTK GATHER FILE
            df_cov = pd.read_csv(f"{gtdbtk_gather}/geomosaic_samples/{s}.tsv", sep="\t")
            df_cov = df_cov.loc[:, ["MAGs", "phylum", "class", "order", "family", "genus", "species"]]

            m = pd.merge(df_mtd, df_cov, how="left", on="MAGs")

            DF_NORM[mtd][s] = m
    
    return DF_NORM
