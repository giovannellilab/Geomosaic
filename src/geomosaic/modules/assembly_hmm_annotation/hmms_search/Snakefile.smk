
rule hmms_search:
    input:
        orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True),
        orf_simple_mapping = expand("{wdir}/{sample}/{orf_prediction}/simple_orf_contig_mapping.tsv", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True), 
        coverage_folder = expand("{wdir}/{sample}/{assembly_coverage}", assembly_coverage=config["MODULES"]["assembly_coverage"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/{assembly_hmmsearch_output_folder}"),
    params:
        hmm_folder=config["ADDITIONAL_PARAM"]["hmm_folder"],
        local_sample="{sample}",
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["hmms_search"])) ) (config["USER_PARAMS"]["hmms_search"]), 
    threads: config["threads"]
    run:
        shell("mkdir -p {output.folder}")
        shell("echo '{params.hmm_folder}' > {output.folder}/hmm_folder_path.txt")

        import pandas as pd
        df_mapping = pd.read_csv(str(input.orf_simple_mapping), sep="\t")

        coverage_methods = []
        with open(os.path.join(str(input.coverage_folder), "list.txt")) as fd:
            for line in fd:
                coverage_methods.append(line.rstrip("\n"))

        list_output_files = []
        for hmm in os.listdir(params.hmm_folder):
            if not hmm.endswith(('.hmm', '.HMM')):
                continue
            
            if hmm.endswith('.hmm'):
                filename=hmm.split(".hmm")[0]
            else:
                filename=hmm.split(".HMM")[0]

            out_path=os.path.join(output.folder, "output_hmms", filename)
            shell("mkdir -p {out_path}")

            hmm_file=os.path.join(params.hmm_folder, hmm)
            shell("hmmsearch --tblout /dev/null -o {out_path}/hmmsearch_output.txt {params.user_params} --cpu {threads} --notextw {hmm_file} {input.orf_predicted}") 
            if os.stat(os.path.join(out_path, "hmmsearch_output.txt")).st_size == 0:
                continue

            list_output_files.append(str(os.path.join(out_path, "hmmsearch_output.txt")))

        from geomosaic.parser.make_hmmsearch_dataframe import make_hmmsearch_dataframe
        df_hmmresults = make_hmmsearch_dataframe(list_output_files)
        df_hmmresults.drop_duplicates(inplace=True)
        df_hmmresults.to_csv(os.path.join(output.folder, "hmmsearch_results.tsv"), sep="\t", header=True, index=False)

        m1 = df_hmmresults.merge(df_mapping, on="orf_id", how="left")

        for mtd in coverage_methods:
            df_coverage = pd.read_csv(os.path.join(str(input.coverage_folder), f"{mtd}.tsv"), sep="\t")
            df_coverage = df_coverage.iloc[:, :2]
            df_coverage.columns = ['contig', mtd]
            temp = pd.merge(m1, df_coverage, how="left", on="contig")
            m1 = temp.copy()
        
        m1["sample"] = str(params.local_sample)

        m1.to_csv(os.path.join(output.folder, "HMMs_coverage_table.tsv"), sep="\t", header=True, index=False)
        shell("( cd {output.folder} && rm -r output_hmms )")
