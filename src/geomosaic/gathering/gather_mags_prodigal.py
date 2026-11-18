import pandas as pd
from subprocess import check_call
import os
from geomosaic.gathering.utils import get_sample_with_results
import shutil

def gather_mags_prodigal(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mags_prodigal"
    
    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    copy_mags(geomosaic_wdir, output_folder, samples, pckg)



def check_mags(folder, output_folder, sample, pckg):

    sample_dir = os.path.join(folder, sample, pckg)
    ok_file = os.path.join(sample_dir, "gather_OK.txt")
    mags_tsv = os.path.join(sample_dir, "MAGs.tsv")
    
    if not os.path.exists(mags_tsv):
        print(f"Sample {sample}: MAGs.tsv not found, skipping.")
        return []
        

    mags_df = pd.read_csv(mags_tsv, sep="\t", dtype=str)
    mags_list = mags_df["MAGs"].tolist()

    valid_mags = []

    if not os.path.exists(ok_file):
        print(f"Sample {sample}: gather_OK.txt not found, check possible missing mags on missing_mags_{sample}.log")

        for mag_id in mags_list:
            src_path = os.path.join(sample_dir, mag_id, "orf_predicted.faa")

            if not os.path.isfile(src_path):
                with open(os.path.join(output_folder, f"missing_mags_{sample}.log"), "a") as f:   
                    f.write(f"{sample} - {src_path}\n")
                continue

            valid_mags.append(mag_id)
    else:
        valid_mags = mags_list

    return valid_mags


def copy_mags(folder, output_folder, samples, pckg):

    for s in samples:

        sample_dir = os.path.join(folder, s, pckg)
        mags_list = check_mags(folder, output_folder, s, pckg)

        for mag_id in mags_list:

            src_path = os.path.join(sample_dir, mag_id, "orf_predicted.faa")
            
            new_mag_name = f"{s}-{mag_id}.faa"
            dst_path = os.path.join(output_folder, new_mag_name)
            shutil.copy(src_path, dst_path)