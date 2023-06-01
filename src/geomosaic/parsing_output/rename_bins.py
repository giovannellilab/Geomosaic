
from subprocess import check_call
import os


def rename_bins(folder, extension, binner):
    for idx, f in enumerate(sorted(os.listdir(folder)), start=1):
        if not f.endswith(f".{extension}"):
            continue
        
        path_file = os.path.join(folder, f)
        new_name = os.path.join(folder, f"{binner}_{idx}.fasta")

        check_call(f"mv {path_file} {new_name}", shell=True)
