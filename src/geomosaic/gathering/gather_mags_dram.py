import pandas as pd
import numpy as np
from subprocess import check_call
from os import listdir
import yaml
import os
from geomosaic.gathering.utils import get_sample_with_results


def gather_mags_dram(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mags_dram"

    samples = get_sample_with_results(pckg, geomosaic_wdir,all_samples)

    output_folder = os.path.join(output_base_folder, pckg)
    check_call(f"mkdir -p {output_folder}", shell=True)

    complete_mags_dram(geomosaic_wdir, output_folder, samples)


def complete_mags_dram(folder, base_output_folder, samples):
    for s in samples:
        parse_for_mags(folder, base_output_folder, s)
        parse_dram_by_cols(folder, base_output_folder, s)


def parse_for_mags(folder, base_output_folder, s):
    df = pd.read_excel(os.path.join(folder,s,"mags_dram","dram_distillation","metabolism_summary.xlsx"))
    
    mags_cols = ["gene_id"] + list(df.columns)[5:]
    df = df.loc[:, mags_cols]
    
    df.drop_duplicates(inplace=True)
    output_folder = os.path.join(base_output_folder, s)
    check_call(f"mkdir -p {output_folder}", shell=True)

    df.rename(columns={"gene_id": "ko_number"}, inplace=True)
    df.to_csv(os.path.join(output_folder,"metabolism_summary.tsv"), sep="\t", index=False, header=True)


def parse_dram_by_cols(folder, base_output_folder, s):
    prod = pd.read_csv(os.path.join(folder,s,"mags_dram","dram_distillation","product.tsv"), sep="\t")
    dram_cols = get_dram_cols()

    output_folder = os.path.join(base_output_folder, s)
    check_call(f"mkdir -p {output_folder}", shell=True)

    for tag, tag_cols in dram_cols.items():
        tag_prod = prod.loc[:,["genome"]+tag_cols].copy()
        tag_prod.drop_duplicates(inplace=True)
        tag_prod.to_csv(os.path.join(output_folder,f"{tag}.tsv"), sep="\t", index=False, header=True)


def get_dram_cols():
    return {
        "modules" : [
            '3-Hydroxypropionate bi-cycle',
            'Acetyl-CoA pathway, CO2 => acetyl-CoA',
            'Citrate cycle (TCA cycle, Krebs cycle)',
            'Dicarboxylate-hydroxybutyrate cycle',
            'Entner-Doudoroff pathway, glucose-6P => glyceraldehyde-3P + pyruvate',
            'Glycolysis (Embden-Meyerhof pathway), glucose => pyruvate',
            'Glyoxylate cycle',
            'Hydroxypropionate-hydroxybutylate cycle',
            'Methanogenesis, CO2 => methane',
            'Pentose phosphate pathway (Pentose phosphate cycle)',
            'Reductive acetyl-CoA pathway (Wood-Ljungdahl pathway)',
            'Reductive citrate cycle (Arnon-Buchanan cycle)',
            'Reductive pentose phosphate cycle (Calvin cycle)',
        ],

        "complex_1": [
            'Complex I: NAD(P)H:quinone oxidoreductase, chloroplasts and cyanobacteria',
            'Complex I: NADH dehydrogenase (ubiquinone) 1 alpha subcomplex',
            'Complex I: NADH:quinone oxidoreductase, prokaryotes',
        ],

        "complex_2": [
            'Complex II: Fumarate reductase, prokaryotes',
            'Complex II: Succinate dehydrogenase (ubiquinone)',
            'Complex II: Succinate dehydrogenase, prokaryotes',
        ],

        "complex_3": [
            'Complex III: Cytochrome bc1 complex',
            'Complex III: Cytochrome bc1 complex respiratory unit',
            'Complex III: Cytochrome bd ubiquinol oxidase',
        ],

        "complex_4": [
            'Complex IV High affinity: Cytochrome bd ubiquinol oxidase',
            'Complex IV High affinity: Cytochrome c oxidase, cbb3-type',
            'Complex IV Low affinity: Cytochrome aa3-600 menaquinol oxidase',
            'Complex IV Low affinity: Cytochrome c oxidase',
            'Complex IV Low affinity: Cytochrome c oxidase, prokaryotes',
            'Complex IV Low affinity: Cytochrome o ubiquinol oxidase',
        ],

        "complex_5": [
            'Complex V: F-type ATPase, eukaryotes',
            'Complex V: F-type ATPase, prokaryotes and chloroplasts',
            'Complex V: V-type ATPase, eukaryotes',
            'Complex V: V/A-type ATPase, prokaryotes',
        ],

        "cazy": [
            'CAZy: Alpha-galactans',
            'CAZy: Alpha-mannan',
            'CAZy: Amorphous Cellulose',
            'CAZy: Arabinan',
            'CAZy: Arabinose cleavage',
            'CAZy: Beta-galactan (pectic galactan)',
            'CAZy: Beta-mannan',
            'CAZy: Chitin',
            'CAZy: Crystalline Cellulose',
            'CAZy: Fucose Cleavage',
            'CAZy: Mixed-Linkage glucans',
            'CAZy: Mucin',
            'CAZy: Pectin',
            'CAZy: Polyphenolics',
            'CAZy: Rhamnose cleavage',
            'CAZy: Starch',
            'CAZy: Sulf-Polysachharides',
            'CAZy: Xylans',
            'CAZy: Xyloglucan',
        ],

        "methanogenesis": [
            'Methanogenesis and methanotrophy: Key functional gene',
            'Methanogenesis and methanotrophy: acetate => methane, pt 1',
            'Methanogenesis and methanotrophy: acetate => methane, pt 2',
            'Methanogenesis and methanotrophy: acetate => methane, pt 3',
            'Methanogenesis and methanotrophy: dimethylamine => monomethylamine',
            'Methanogenesis and methanotrophy: methane => methanol, with oxygen (mmo)',
            'Methanogenesis and methanotrophy: methane => methanol, with oxygen (pmo)',
            'Methanogenesis and methanotrophy: methanol => methane',
            'Methanogenesis and methanotrophy: monomethylamine => ammonia',
            'Methanogenesis and methanotrophy: putative but not defining CO2 => methane',
            'Methanogenesis and methanotrophy: trimethylamine => dimethylamine',
        ],

        "nitrogen_metab": [
            'Nitrogen metabolism: Bacterial (aerobic-specific) ammonia oxidation',
            'Nitrogen metabolism: Bacterial (anaerobic-specific) ammonia oxidation',
            'Nitrogen metabolism: Bacterial/Archaeal ammonia oxidation',
            'Nitrogen metabolism: Dissimilatory nitrite reduction to ammonia (DNRA)',
            'Nitrogen metabolism: Nitrogen fixation altennative',
            'Nitrogen metabolism: ammonia => nitrite',
            'Nitrogen metabolism: nitrate => nitrite',
            'Nitrogen metabolism: nitric oxide => nitrous oxide',
            'Nitrogen metabolism: nitrite => nitric oxide',
            'Nitrogen metabolism: nitrite=> nitrate',
            'Nitrogen metabolism: nitrogen => ammonia',
            'Nitrogen metabolism: nitrous oxide => nitrogen',
        ],

        "other_reductases": [
            'Other Reductases: TMAO reductase',
            'Other Reductases: arsenate reduction, pt 1',
            'Other Reductases: arsenate reduction, pt 2',
            'Other Reductases: mercury reduction',
            'Other Reductases: selenate/Chlorate reduction',
        ],

        "photosynthesis": [
            'Photosynthesis: Photosystem I',
            'Photosynthesis: Photosystem II',
        ],

        "scfa": [
            'SCFA and alcohol conversions: Alcohol production',
            'SCFA and alcohol conversions: Butyrate, pt 1',
            'SCFA and alcohol conversions: Butyrate, pt 2',
            'SCFA and alcohol conversions: Propionate, pt 1',
            'SCFA and alcohol conversions: Propionate, pt 2',
            'SCFA and alcohol conversions: acetate, pt 1',
            'SCFA and alcohol conversions: acetate, pt 2',
            'SCFA and alcohol conversions: acetate, pt 3',
            'SCFA and alcohol conversions: lactate D',
            'SCFA and alcohol conversions: lactate L',
            'SCFA and alcohol conversions: pyruvate => acetyl CoA v1',
            'SCFA and alcohol conversions: pyruvate => acetyl CoA v2',
            'SCFA and alcohol conversions: pyruvate => acetylCoA f+ formate v3',
        ],

        "sulfur": [
            'Sulfur metabolism: Thiosulfate oxidation by SOX complex, thiosulfate => sulfate',
            'Sulfur metabolism: dissimilatory sulfate reduction (and oxidation) sulfate => sulfide',
            'Sulfur metabolism: tetrathionate => thiosulfate',
            'Sulfur metabolism: thiosulfate => sulfite',
        ]
    }
