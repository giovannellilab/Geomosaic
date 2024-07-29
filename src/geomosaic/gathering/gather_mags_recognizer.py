import pandas as pd
import numpy as np
from subprocess import check_call
from os import listdir
import os
import yaml
from geomosaic.gathering.gather_recognizer import get_dtypes
from geomosaic.gathering.utils import get_sample_with_results


def gather_mags_recognizer(config_file, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mags_recognizer"

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    samples = get_sample_with_results(pckg, geomosaic_wdir, config["SAMPLES"])

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_mags_recognizer(geomosaic_wdir, output_folder, samples)


def complete_mags_recognizer(folder, output_folder, samples):
    for s in samples:
        cog = parse_quantification(folder, s, filename = "COG_quantification.tsv", pivot="COG_id")
        check_call(f"mkdir -p {output_folder}/{s}", shell=True)
        cog.to_csv(f"{output_folder}/{s}/COG_quantification.tsv", header=True, index=False, sep="\t")

        kog = parse_quantification(folder, s, filename = "KOG_quantification.tsv", pivot="KOG_id")
        check_call(f"mkdir -p {output_folder}/{s}", shell=True)
        kog.to_csv(f"{output_folder}/{s}/KOG_quantification.tsv", header=True, index=False, sep="\t")

        parse_mags_recognizer_EC_KO(folder, output_folder, s)


def parse_mags_recognizer_EC_KO(folder, output_folder, s):
    results_folder = f"{folder}/{s}/mags_recognizer"
    
    DFs_ec = []
    DFs_ko = []
    
    unique_ec = set()
    unique_ko = set()
    for m in listdir(results_folder):
        folder_data = f"{results_folder}/{m}"
        if not os.path.isdir(folder_data) or not m.startswith("mag_"):
            continue

        if "reCOGnizer_results.tsv" not in listdir(f"{folder_data}"):
            continue
            
        df = pd.read_csv(f"{folder_data}/reCOGnizer_results.tsv", sep="\t", dtype=get_dtypes())
        c1 = df["pident"] > 80
        c2 = df["gapopen"] < 5
        
        relia = df[c1 & c2].copy()
        if relia.shape[0] == 0:
            continue

        check_call(f"mkdir -p {output_folder}/{s}", shell=True)
        
        relia.drop_duplicates(inplace=True)
        
        ec = clean_recognizer_dataframe(relia, m, "EC number", delim=",")
        unique_ec.update(list(ec["EC number"].unique()))
        DFs_ec.append(ec)
        
        ko = clean_recognizer_dataframe(relia, m, "KO", delim=";")
        unique_ko.update(list(ko["KO"].unique()))
        DFs_ko.append(ko)
        
    if len(DFs_ec) > 0:
        final_ec = compose_final_matrix(DFs_ec, unique_ec, "EC number")
        final_ec.to_csv(f"{output_folder}/{s}/EC_number.tsv", sep="\t", index=False, header=True)

    if len(DFs_ko) > 0:
        final_ko = compose_final_matrix(DFs_ko, unique_ko, "KO")
        final_ko.to_csv(f"{output_folder}/{s}/KO.tsv", sep="\t", index=False, header=True)


def clean_recognizer_dataframe(df, s, pivot, delim):
    df_parsed = df[df[pivot] == df[pivot]].loc[:, ["qseqid", pivot]]
    df_parsed = df_parsed[df_parsed[pivot] != "-"]
    
    df_parsed[pivot] = df_parsed[pivot].str.split(delim)
    df_parsed = df_parsed.explode(pivot)

    df_parsed.drop_duplicates(inplace=True)

    res = df_parsed.groupby(pivot).count().reset_index()
    res.rename(columns = {"qseqid": s}, inplace=True)
    return res


def compose_final_matrix(list_dfs, unique_list, pivot):
    m = pd.DataFrame(sorted(unique_list), columns=[pivot])
    for x in list_dfs:
        temp = pd.merge(m, x, how="left", on=pivot)
        m = temp.copy()
    
    finalm = m.replace(np.nan, 0, regex=True)
    return finalm


def parse_quantification(folder, s, filename, pivot):
    DFs_cog = []
    unique_cog = set()

    results_folder = f"{folder}/{s}/mags_recognizer"
    
    for m in sorted(listdir(results_folder)):
        folder_data = f"{results_folder}/{m}"
        if not os.path.isdir(folder_data) or not m.startswith("mag_"):
            continue
        
        if filename not in listdir(f"{folder_data}"):
            continue
        
        fn = f"{folder_data}/{filename}"
        cog = pd.read_csv(fn, 
                          sep="\t", names=["counts", "class", "subclass", "descr", pivot])

        unique_cog.update(list(cog[["class", "subclass", "descr", pivot]].itertuples(index=False, name=None)))
        cog.rename(columns={"counts": m}, inplace=True)
        DFs_cog.append(cog)

    merged = pd.DataFrame(sorted(unique_cog), columns=["class", "subclass", "descr", pivot])
    for x in DFs_cog:
        temp = pd.merge(merged, x, how="left", on=["class", "subclass", "descr", pivot])
        merged = temp.copy()

    finalm = merged.replace(np.nan, 0, regex=True)
        
    return finalm
