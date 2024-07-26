
import pandas as pd
from Bio.SeqIO.FastaIO import SimpleFastaParser
from geomosaic._utils import GEOMOSAIC_NOTE
from subprocess import check_call


def retrieve_survival_mags(checkm_table, das_tool_bins, completness_threshold, contamination_threshold, outfolder, mags_general_file):
    df = pd.read_csv(checkm_table, sep="\t")
    df["Completeness"] = df["Completeness"].astype("float64")
    df["Contamination"] = df["Contamination"].astype("float64")

    c1 = df["Completeness"] >= completness_threshold
    c2 = df["Contamination"] <= contamination_threshold

    df_mags = df[c1 & c2].copy()
    if df_mags.shape[0] == 0:
        print(f"\n{GEOMOSAIC_NOTE}: There are no MAGs that satisfy the thresholds in Completeness and Contamination. Try to lower these values. SystemExit.\n")
        exit(0)

    mags_col = [f"mag_{idx}" for idx in range(1, len(df_mags)+1)]
    df_mags.insert(0, 'MAGs', mags_col)

    df_mags.rename(columns={'Bin Id': 'binID'}, inplace=True)
    df_mags.to_csv(f"{outfolder}/MAGs.tsv", header=True, index=False, sep="\t")
    df_mags.to_csv(mags_general_file, header=True, index=False, sep="\t")
    mags_list = {}

    for i in df_mags.itertuples():
        local_key = i.MAGs
        local_mag = []
        with open(f"{das_tool_bins}/{i.binID}.fa") as fd:
            for header, seq in SimpleFastaParser(fd):
                local_header = f"{local_key}_{header}"
                local_mag.append((i, local_header, seq))

        mags_list[local_key] = local_mag
    
    for key, mag in mags_list.items():
        with open(f"{outfolder}/fasta/{key}.fa", "wt") as fo:
            for _, header, seq in mag:
                fo.write(f">{header}\n{seq}\n")
    