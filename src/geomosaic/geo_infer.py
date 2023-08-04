import os
import pandas as pd
from geomosaic._utils import GEOMOSAIC_ERROR


def geo_infer(args):
    folder_rawreads     = args.directory
    output_path         = args.output_path
    split_token         = args.split_token

    if " " in split_token:
        print(f"{GEOMOSAIC_ERROR}: 'split_tokens' parameter must not contain space")
        exit(1)

    df_samples = infer_samples_list(folder_rawreads, split_token)
    df_samples.to_excel(f"{output_path}/geomosaic_inferred_sample_list.xlsx", header=True, index=False)


def infer_samples_list(folder_rawreads, split_token):
    l = []

    st_r1, st_r2 = split_token.split(",")

    all_found_files = sorted(os.listdir(folder_rawreads))

    for f in all_found_files:
        if st_r1 in f:
            prefix, suffix = f.split(st_r1)
            f2 = f"{prefix}{st_r2}{suffix}"

            if f2 in all_found_files:
                sample_name = f.split("_")[0]
                l.append((f, f2, sample_name))

    return pd.DataFrame(l, columns=["r1", "r2", "inferred_sample_name"])
