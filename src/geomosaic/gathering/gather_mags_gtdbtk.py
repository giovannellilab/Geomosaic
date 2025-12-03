import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_mags_gtdbtk(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mags_gtdbtk"
    
    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_mags_gtdbtk(geomosaic_wdir, output_folder, samples)


def complete_mags_gtdbtk(folder, output_folder, samples):
    DF_TAXA_RANKS = get_tax_info(folder, output_folder, samples)

    domain_merged = merge_results_by_taxa(DF_TAXA_RANKS, taxa_level="domain")
    domain_merged.to_csv(os.path.join(output_folder,"domain.tsv"), sep="\t", header=True, index=False)

    phylum_merged = merge_results_by_taxa(DF_TAXA_RANKS, taxa_level="phylum")
    phylum_merged.to_csv(os.path.join(output_folder,"phylum.tsv"), sep="\t", header=True, index=False)

    class_merged = merge_results_by_taxa(DF_TAXA_RANKS, taxa_level="class")
    class_merged.to_csv(os.path.join(output_folder,"class.tsv"), sep="\t", header=True, index=False)

    order_merged = merge_results_by_taxa(DF_TAXA_RANKS, taxa_level="order")
    order_merged.to_csv(os.path.join(output_folder,"order.tsv"), sep="\t", header=True, index=False)

    family_merged = merge_results_by_taxa(DF_TAXA_RANKS, taxa_level="family")
    family_merged.to_csv(os.path.join(output_folder,"family.tsv"), sep="\t", header=True, index=False)

    genus_merged = merge_results_by_taxa(DF_TAXA_RANKS, taxa_level="genus")
    genus_merged.to_csv(os.path.join(output_folder,"genus.tsv"), sep="\t", header=True, index=False)

    species_merged = merge_results_by_taxa(DF_TAXA_RANKS, taxa_level="species")
    species_merged.to_csv(os.path.join(output_folder,"species.tsv"), sep="\t", header=True, index=False)


def get_tax_info(base_folder, output_folder, samples):
    DF_TAXA_RANKS = {
        "domain": {},
        "phylum": {},
        "class": {},
        "order": {},
        "family": {},
        "genus": {},
        "species": {},
    }

    taxa_ranks = ["domain", "phylum", "class", "order", "family", "genus", "species"]

    for s in samples:
        results_folder = os.path.join(base_folder,s,"mags_gtdbtk")
        
        flag_bac = False
        if "gtdbtk.bac120.summary.tsv" in listdir(results_folder):
            flag_bac = True
        
            bac_df = pd.read_csv(os.path.join(results_folder,"gtdbtk.bac120.summary.tsv"), sep="\t")
            
            bac_df["domain"]  = bac_df.apply(lambda x: get_taxa_ranks(x["classification"], "domain"), axis=1)
            bac_df["phylum"]  = bac_df.apply(lambda x: get_taxa_ranks(x["classification"], "phylum"), axis=1)
            bac_df["class"]   = bac_df.apply(lambda x: get_taxa_ranks(x["classification"], "class"), axis=1)
            bac_df["order"]   = bac_df.apply(lambda x: get_taxa_ranks(x["classification"], "order"), axis=1)
            bac_df["family"]  = bac_df.apply(lambda x: get_taxa_ranks(x["classification"], "family"), axis=1)
            bac_df["genus"]   = bac_df.apply(lambda x: get_taxa_ranks(x["classification"], "genus"), axis=1)
            bac_df["species"] = bac_df.apply(lambda x: get_taxa_ranks(x["classification"], "species"), axis=1)

        flag_arc = False
        if "gtdbtk.ar53.summary.tsv" in listdir(results_folder):
            flag_arc = True
            
            arc_df = pd.read_csv(os.path.join(results_folder,"gtdbtk.ar53.summary.tsv"), sep="\t")
            
            arc_df["domain"]  = arc_df.apply(lambda x: get_taxa_ranks(x["classification"], "domain"), axis=1)
            arc_df["phylum"]  = arc_df.apply(lambda x: get_taxa_ranks(x["classification"], "phylum"), axis=1)
            arc_df["class"]   = arc_df.apply(lambda x: get_taxa_ranks(x["classification"], "class"), axis=1)
            arc_df["order"]   = arc_df.apply(lambda x: get_taxa_ranks(x["classification"], "order"), axis=1)
            arc_df["family"]  = arc_df.apply(lambda x: get_taxa_ranks(x["classification"], "family"), axis=1)
            arc_df["genus"]   = arc_df.apply(lambda x: get_taxa_ranks(x["classification"], "genus"), axis=1)
            arc_df["species"] = arc_df.apply(lambda x: get_taxa_ranks(x["classification"], "species"), axis=1)

        if not flag_bac and not flag_arc:
            continue

        check_call(f"mkdir -p {output_folder}/geomosaic_samples", shell=True)
        
        if flag_arc and flag_bac:
            final = pd.concat([bac_df, arc_df], ignore_index=True, )
        elif flag_arc and not flag_bac:
            final = arc_df
        else:
            assert flag_bac and not flag_arc
            final = bac_df

        final.rename(columns={"user_genome": "MAGs"}, inplace=True)
        final.loc[:, ["MAGs", "domain", "phylum", "class", "order", "family", "genus", "species", "classification"]].to_csv(
            f"{output_folder}/geomosaic_samples/{s}.tsv", 
            sep="\t", header=True, index=False
        )
        
        for tr in taxa_ranks:
            DF_TAXA_RANKS[tr][s] = final.loc[:,[tr, "MAGs"]].groupby(by=tr).count().reset_index()
        
    return DF_TAXA_RANKS


def merge_results_by_taxa(DF_TAXA_RANKS, taxa_level):
    assert taxa_level in ["domain", "phylum", "class", "order", "family", "genus", "species"]
    
    # remove empty classification
    for _, x in DF_TAXA_RANKS[taxa_level].items():
        x.replace(r'^\s*$', "unclassified_", regex=True, inplace=True)
    
    db_list = []
    for _, x in DF_TAXA_RANKS[taxa_level].items():
        db_list += list(x[taxa_level])
    
    unique_db_list = sorted(set(db_list))
    
    m = pd.DataFrame(unique_db_list, columns=[taxa_level])
    
    for s, x in DF_TAXA_RANKS[taxa_level].items():
        temp_sample_df = x.copy()
        temp_sample_df.rename(columns={"MAGs": s}, inplace=True)
        temp = pd.merge(m, temp_sample_df, how="left", on=taxa_level)
        m = temp.copy()
    
    newm = m.fillna(0)
    return newm


def get_taxa_ranks(classification, taxa_rank="all"):
    mapping = {
        "domain": 'd',
        "phylum": 'p',
        "class": 'c',
        "order": 'o',
        "family": 'f',
        "genus": 'g',
        "species": 's',
    }
    
    tokens = classification.split(";")
    d = {}
    for tkn in tokens:
        rank = tkn[0]
        info = tkn[3:]
        
        d[rank] = info
    
    if taxa_rank == "all":
        return d
    elif taxa_rank == "domain":
        return d[mapping[taxa_rank]]
    elif taxa_rank == "phylum":
        return d[mapping[taxa_rank]]
    elif taxa_rank == "class":
        return d[mapping[taxa_rank]]
    elif taxa_rank == "order":
        return d[mapping[taxa_rank]]
    elif taxa_rank == "family":
        return d[mapping[taxa_rank]]
    elif taxa_rank == "genus":
        return d[mapping[taxa_rank]]
    else:
        assert taxa_rank == "species"
        return d[mapping[taxa_rank]]
