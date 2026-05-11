import os
import glob
import pandas as pd
from subprocess import check_call
from geomosaic.gathering.utils import get_sample_with_results


def gather_kofam_scan(all_samples, geomosaic_wdir, output_base_folder, additional_info):
    
    pckg = "kofam_scan"
    
    samples = get_sample_with_results(pckg, geomosaic_wdir, all_samples)

    output_folder = os.path.join(output_base_folder, pckg)
    
    check_call(f"mkdir -p {output_folder}", shell=True)
    compose_matrix_kofam_scan(geomosaic_wdir, output_folder, samples, pckg)


def compose_matrix_kofam_scan(folder, output_folder, samples, pckg):
    """
    Processes KOfam scan result files for all samples and writes 4 output files:
      1. geomosaic-kofam_scan.csv                          — all hits (long)
      2. geomosaic-kofam_scan-counts-by-orf.csv            — counts per ORF
      3. geomosaic-kofam_scan-by-sample-long/wide.csv      — counts grouped by sample
      4. geomosaic-kofam_scan-by-sample-long/wide.csv — counts grouped by sample
    """
    all_hits = []

    for sample in samples:

        glob_pattern = os.path.join(folder, sample, pckg, "result.txt")

        for filename in glob.glob(glob_pattern, recursive=True):
            kofam_df = pd.read_table(filename)

            # Drop the blank separator line that KOfam inserts
            kofam_df = kofam_df.iloc[1:]

            # Keep only hits that pass the built-in threshold (marked with "*" in "#" column)
            # kofam_df = kofam_df.dropna(subset=["#"])

            kofam_df = kofam_df.rename(columns={
                "gene name": "gene_name",
                "ko definition": "ko_definition",
            })

            kofam_df["sample"] = sample

            all_hits.append(kofam_df)

    if not all_hits:
        print(f"[!] No KOfam results found for package '{pckg}' — skipping.")
        return

    final_df = pd.concat(all_hits, ignore_index=True)

    id_cols = ["sample"]
    final_df = final_df[id_cols + [c for c in final_df.columns if c not in id_cols]]

    # Output 1 – full hit table
    
    _write_csv(final_df, output_folder, f"geomosaic-{pckg}.csv",
               label="all hits")
 
    # Output 2 – counts per ORF  (sample × gene_name)

    counts_orf = (
        final_df
        .value_counts(["sample", "gene_name"])
        .reset_index()
        .rename(columns={0: "count"})
    )
    _write_csv(counts_orf, output_folder, f"geomosaic-{pckg}-counts-by-orf.csv",
               label="counts per ORF")
 
    # Output 3 – long + wide tables grouped by sample

    group_df = (
        final_df
        .groupby(["KO", "sample"], as_index=False)
        .size()
        .rename(columns={"size": "count"})
    )
 
    wide_df = (
        group_df
        .pivot(index="sample", columns="KO", values="count")
        .reset_index()
        .fillna(0.0)
    )
 
    _write_csv(group_df, output_folder, f"geomosaic-{pckg}-by-sample-long.csv",
               label="counts by sample (long)")
    _write_csv(wide_df, output_folder, f"geomosaic-{pckg}-by-sample-wide.csv",
               label="counts by sample (wide)")
 
 
def _write_csv(df: pd.DataFrame, folder: str, filename: str, label: str = "") -> None:
    path = os.path.join(folder, filename)
    df.to_csv(path, index=False)
    tag = f" ({label})" if label else ""
    print(f"[+] KOfam results{tag} written to {path}")