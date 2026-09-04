import pandas as pd
from subprocess import check_call
from os import listdir
import os
from geomosaic.gathering.utils import get_sample_with_results


def gather_mags_kofam_scan_redox_metal_plasticity_index(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mags_kofam_scan_redox_metal_plasticity_index"

    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    complete_mags_kofam_scan_redox_metal_plasticity_index(geomosaic_wdir, pckg, output_folder, samples)


def complete_mags_kofam_scan_redox_metal_plasticity_index(folder, pckg, base_output_folder, samples):
    for s in samples:
        All_mags_df = parse_redox_metal_plasticity_index_mags(folder, pckg, s)

        output_folder = os.path.join(base_output_folder, s)
        check_call(f"mkdir -p {output_folder}", shell=True)

        for t in ['redox_metal_indexes', 'redox_metal_indexes_extended']:
            if not All_mags_df[t]:
                continue

            concat = pd.concat(All_mags_df[t], ignore_index=True)
            concat.to_csv(os.path.join(output_folder, f"ALL_MAGs_{t}.tsv"), sep="\t", header=True, index=False)


def parse_redox_metal_plasticity_index_mags(folder, pckg, s):
    All_mags_df = {'redox_metal_indexes': [], 'redox_metal_indexes_extended': []}

    results_folder = os.path.join(folder, s, pckg)
    for m in listdir(results_folder):
        folder_data = os.path.join(results_folder, m, "metabolic_index")
        if not os.path.isdir(folder_data) or not m.startswith("mag_"):
            continue

        for t in All_mags_df:
            if f"{t}.tsv" not in listdir(folder_data):
                continue

            df = pd.read_csv(os.path.join(folder_data, f"{t}.tsv"), sep="\t")
            All_mags_df[t].append(df)

    return All_mags_df