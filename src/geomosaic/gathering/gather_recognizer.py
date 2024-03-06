import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from numpy import float64



def gather_recognizer(config_file, geomosaic_wdir, output_base_folder):
    pckg = "recognizer"

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    samples = config["SAMPLES"]

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_recognizer(geomosaic_wdir, output_folder, samples)


def complete_recognizer(folder, output_folder, samples):
    DFs_ec = []
    DFs_ko = []

    unique_ec = set()
    unique_ko = set()

    for s in samples:
        folder_data = f"{folder}/{s}/recognizer"

        flag = True
        if "reCOGnizer_results.tsv" not in listdir(folder_data):
            flag = False
            break
            
        df = pd.read_csv(f"{folder_data}/reCOGnizer_results.tsv", sep="\t", dtype=get_dtypes())
        c1 = df["pident"] > 80
        c2 = df["gapopen"] < 5
        
        relia = df[c1 & c2].copy()
        relia.drop_duplicates(inplace=True)
        
        ec = parse_recognizer_results(relia, s, "EC number", delim=",")
        unique_ec.update(list(ec["EC number"].unique()))
        DFs_ec.append(ec)
        
        ko = parse_recognizer_results(relia, s, "KO", delim=";")
        unique_ko.update(list(ko["KO"].unique()))
        DFs_ko.append(ko)
        
        
    if flag:
        final_ec = compose_final_matrix(DFs_ec, unique_ec, "EC number")
        final_ec.to_csv(f"{output_folder}/EC_number.tsv", sep="\t", index=False, header=True)
        
        final_ko = compose_final_matrix(DFs_ko, unique_ko, "KO")
        final_ko.to_csv(f"{output_folder}/KO.tsv", sep="\t", index=False, header=True)
    
    cog = parse_recognizer_quantification(folder, samples, filename="COG_quantification.tsv", pivot="COG_id")
    cog.to_csv(f"{output_folder}/COG_quantification.tsv", header=True, index=False, sep="\t")

    kog = parse_recognizer_quantification(folder, samples, filename="KOG_quantification.tsv", pivot="KOG_id")
    kog.to_csv(f"{output_folder}/KOG_quantification.tsv", header=True, index=False, sep="\t")


def parse_recognizer_results(df, s, pivot, delim):
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


def parse_recognizer_quantification(folder, samples, filename, pivot):
    DFs_cog = []
    unique_cog = set()

    for s in samples:
        fn = f"{folder}/{s}/recognizer/{filename}"
        cog = pd.read_csv(fn, 
                          sep="\t", names=["counts", "class", "subclass", "descr", pivot])

        unique_cog.update(list(cog[["class", "subclass", "descr", pivot]].itertuples(index=False, name=None)))
        cog.rename(columns={"counts": s}, inplace=True)
        DFs_cog.append(cog)

    m = pd.DataFrame(sorted(unique_cog), columns=["class", "subclass", "descr", pivot])
    for x in DFs_cog:
        temp = pd.merge(m, x, how="left", on=["class", "subclass", "descr", pivot])
        m = temp.copy()

    finalm = m.replace(np.nan, 0, regex=True)
    return finalm



def get_dtypes():
    return {
    "qseqid":  object,
    "DB ID":  object,
    "Protein description":  object,
    "DB description":  object,
    "EC number":  object,
    "CDD ID":  object,
    "taxonomic_range_name":  object,
    "taxonomic_range": float64,
    "Superfamilies":  object,
    "Sites":  object,
    "Motifs":  object,
    "pident": float64,
    "length": float64,
    "mismatch": float64,
    "gapopen": float64,
    "qstart": float64,
    "qend": float64,
    "sstart": float64,
    "send": float64,
    "evalue": float64,
    "bitscore": float64,
    "General functional category":  object,
    "Functional category":  object,
    "KO":  object,
}
