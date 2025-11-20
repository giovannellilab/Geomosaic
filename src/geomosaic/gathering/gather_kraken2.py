import pandas as pd
import numpy as np
from subprocess import check_call
import os
from os import listdir
import yaml
from geomosaic.gathering.utils import get_sample_with_results


def gather_kraken2(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "kraken2"

    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    parse_kraken_report(geomosaic_wdir, output_folder, samples)


def parse_kraken_report(folder, output_folder, samples):
    DF_TAXA_RANKS = load_kraken_files(folder, samples)

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
        temp = pd.merge(m, temp_sample_df, how="left", on=taxa_level)
        m = temp.copy()
    
    newm = m.fillna(0)
    return newm


def load_kraken_files(folder, samples):
    def adjust_scientific_name(string):
        scientific_name = ""
        flag = False
        for c in string:
            if c != " " and not flag:
                flag = True
    
            if flag:
                scientific_name += c
        return scientific_name
    
    cols = [
        "fragments_pecentage_rooted_at_this_taxon",
        "fragments_clade_rooted_at_this_taxon",
        "fragments_of_this_taxon",
        "classification",
        "NCBI_taxon_id",
        "sc. name"
    ]

    DF_TAXA_RANKS = {
        "domain": {},
        "phylum": {},
        "class": {},
        "order": {},
        "family": {},
        "genus": {},
        "species": {},
    }

    for s in samples:
        df = pd.read_csv(os.path.join(folder,s,"kraken2","kraken_report.txt"), sep="\t", names=cols)
        df["scientific_name"] = df.apply(lambda x: adjust_scientific_name(x["sc. name"]), axis=1)
        c1 = df["scientific_name"] != "unclassified"
        c2 = df["scientific_name"] != "root"
        c3 = df["scientific_name"] != "cellular organisms"
        c4 = df["fragments_clade_rooted_at_this_taxon"] > 0
        
        df = df[c1 & c2 & c3 & c4]
        df.drop_duplicates(inplace=True)

        categories = {"domain": "D", "phylum": "P", "class": "C", "order": "O", "family": "F", "genus": "G", "species": "S"}
        
        for cat, cls in categories.items():
            final = df[df["classification"] == cls ].loc[:,["scientific_name", "fragments_clade_rooted_at_this_taxon"]]
            final.rename(columns={"scientific_name": cat, "fragments_clade_rooted_at_this_taxon": s}, inplace=True)
            
            DF_TAXA_RANKS[cat][s] = final

    return DF_TAXA_RANKS
