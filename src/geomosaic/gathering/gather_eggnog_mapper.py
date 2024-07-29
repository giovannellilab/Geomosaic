import pandas as pd
import numpy as np
from subprocess import check_call
from os import listdir
import os
import yaml


def gather_eggnogmapper(config_file, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "eggnog_mapper"

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    samples = config["SAMPLES"]

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    parse_eggonog_files(geomosaic_wdir, output_folder, samples)


def parse_eggonog_files(folder, output_folder, samples):
    DFs_modules = []
    DFs_ko = []
    DFs_reaction = []
    DFs_rclass = []

    unique_modules = set()
    unique_ko = set()
    unique_reaction = set()
    unique_rclass = set()

    for s in samples:
        folder_data = f"{folder}/{s}/eggnog_mapper"

        flag = True
        if "gm_eggnog_annot.emapper.annotations" not in listdir(folder_data):
            flag = False
            break
            
        df = pd.read_csv(f"{folder_data}/gm_eggnog_annot.emapper.annotations", sep="\t", skiprows=4)
        
        a = parse_eggnog_annotation(df, s, "KEGG_Module")
        unique_modules.update(list(a["KEGG_Module"].unique()))
        DFs_modules.append(a)
        
        b = parse_eggnog_annotation(df, s, "KEGG_ko")
        unique_ko.update(list(b["KEGG_ko"].unique()))
        DFs_ko.append(b)
        
        c = parse_eggnog_annotation(df, s, "KEGG_Reaction")
        unique_reaction.update(list(c["KEGG_Reaction"].unique()))
        DFs_reaction.append(c)
        
        d = parse_eggnog_annotation(df, s, "KEGG_rclass")
        unique_rclass.update(list(d["KEGG_rclass"].unique()))
        DFs_rclass.append(d)
    
    if flag:
        final_modules = compose_final_matrix(DFs_modules, unique_modules, "KEGG_Module")
        final_modules.to_csv(f"{output_folder}/KEGG_module.tsv", sep="\t", index=False, header=True)
        
        final_ko = compose_final_matrix(DFs_ko, unique_ko, "KEGG_ko")
        final_ko.to_csv(f"{output_folder}/KEGG_ko.tsv", sep="\t", index=False, header=True)
        
        final_reaction = compose_final_matrix(DFs_reaction, unique_reaction, "KEGG_Reaction")
        final_reaction.to_csv(f"{output_folder}/KEGG_reaction.tsv", sep="\t", index=False, header=True)
        
        final_rclass = compose_final_matrix(DFs_rclass, unique_rclass, "KEGG_rclass")
        final_rclass.to_csv(f"{output_folder}/KEGG_rclass.tsv", sep="\t", index=False, header=True)


def parse_eggnog_annotation(df, s, pivot):
    df_parsed = df[df[pivot] == df[pivot]]
    df_parsed = df_parsed.loc[:, ["#query", pivot]]

    df_parsed = df_parsed[df_parsed[pivot] != "-"]
    
    df_parsed[pivot] = df_parsed[pivot].str.split(',')
    df_parsed = df_parsed.explode(pivot)

    df_parsed.drop_duplicates(inplace=True)

    res = df_parsed.groupby(pivot).count().reset_index()
    res.rename(columns = {"#query": s}, inplace=True)
    return res


def compose_final_matrix(list_dfs, unique_list, pivot):
    m = pd.DataFrame(sorted(unique_list), columns=[pivot])
    for x in list_dfs:
        temp = pd.merge(m, x, how="left", on=pivot)
        m = temp.copy()
    
    finalm = m.replace(np.nan, 0, regex=True)
    return finalm
