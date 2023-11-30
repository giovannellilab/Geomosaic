
rule hmms_cov:
    input:
        orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["orf_prediction"], allow_missing=True),
        orf_simple_mapping = expand("{wdir}/{sample}/{orf_prediction}/simple_orf_contig_mapping.tsv", orf_prediction=config["orf_prediction"], allow_missing=True), 
        covstats_folder=expand("{wdir}/{sample}/{assembly_qc_readmapping}", assembly_qc_readmapping=config["assembly_qc_readmapping"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/hmms_cov")
    params:
        hmm_folder=config["hmm_folder"]
    threads: 5
    run:
        shell("mkdir -p {output.folder}")
        
        import pandas as pd

        df_mapping = pd.read_csv(str(input.orf_simple_mapping), sep="\t")
        df_coverage = pd.read_csv(os.path.join(str(input.covstats_folder), "covstats.tsv"), sep="\t")
        local_sample = output.folder.split("/")[-2]
        total_length = int(df_coverage.Length.sum())
        
        results_filename = f"{output.folder}/coverage_results.tsv"
        with open(results_filename, "wt") as fd:
            fd.write("name\ttotal_coverage\tnormalized_total_coverage\tsample\n")

            for hmm in os.listdir(params.hmm_folder):
                if not hmm.endswith('.hmm'):
                    continue
                
                filename=hmm.split(".hmm")[0]
                out_path=os.path.join(output.folder, filename)
                shell("mkdir -p {out_path}")

                hmm_file=os.path.join(params.hmm_folder, hmm)
                shell("hmmsearch --tblout {out_path}/hmmsearch_table.txt -o /dev/null --cpu {threads} --notextw {hmm_file} {input.orf_predicted}") 
                shell("grep -v \"^#\" {out_path}/hmmsearch_table.txt > {out_path}/results.txt || true")
                if os.stat(os.path.join(out_path, "results.txt")).st_size == 0:
                    continue

                shell("awk '{{print $1\"\t\"$3}}' {out_path}/results.txt > {out_path}/hits.txt")

                df_hits = pd.read_csv(os.path.join(out_path,"hits.txt"), sep="\t", names=["orf_id", "name"])
                df_hits.drop_duplicates(inplace=True)

                m1 = df_hits.merge(df_mapping, on="orf_id", how="left")
                m2 = m1.merge(df_coverage, left_on="contig", right_on="#ID", how="left")

                subset = m2.loc[:, ["orf_id", "name", "contig", "Avg_fold"]]
                subset["Avg_fold"] = subset["Avg_fold"].astype(float)

                total_coverage = subset["Avg_fold"].sum()
                
                name=list(subset.name.unique())[0]
                normalized_total_cov = (total_coverage/total_length)*1000000

                fd.write(f"{name}\t{total_coverage}\t{normalized_total_cov}\t{local_sample}\n")
                
                subset.to_csv(os.path.join(out_path, "orf_coverage.tsv"), sep="\t", header=True, index=False)
