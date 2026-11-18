import pandas as pd
from subprocess import check_call
import os
from geomosaic.gathering.utils import get_sample_with_results
import shutil

def gather_mags(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    pckg = "mags"
    
    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)

    check_call(f"mkdir -p {output_folder}", shell=True)
    copy_mags(geomosaic_wdir, output_folder, samples)



def check_mags(folder, output_folder, sample):

    sample_dir = os.path.join(folder, sample)
    mags_tsv = os.path.join(sample_dir, "mags", "MAGs.tsv")
    
    if not os.path.exists(mags_tsv):
        print(f"Sample {sample}: MAGs.tsv not found, skipping.")
        return []
        

    mags_df = pd.read_csv(mags_tsv, sep="\t", dtype=str)
    mags_list = mags_df["MAGs"].tolist()

    valid_mags = []

    for mag_id in mags_list:
            src_path = os.path.join(sample_dir, "mags", "fasta", f"{mag_id}.fa")

            if not os.path.isfile(src_path):
                with open(os.path.join(output_folder, f"missing_mags_{sample}.log"), "a") as f:   
                    f.write(f"{sample} - {src_path}\n")
                continue

            valid_mags.append(mag_id)

    return valid_mags


def copy_mags(folder, output_folder, samples):

    for s in samples:

        sample_dir = os.path.join(folder, s)
        mags_list = check_mags(folder, output_folder, s)

        for mag_id in mags_list:

            src_path = os.path.join(sample_dir, "mags", "fasta", f"{mag_id}.fa")
            
            new_mag_name = f"{s}-{mag_id}.fna"
            dst_path = os.path.join(output_folder, new_mag_name)
            shutil.copy(src_path, dst_path)