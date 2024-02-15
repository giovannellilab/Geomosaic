
rule run_mags_hmmsearch:
    input:
        mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/orf_predicted.faa", mags_orf_prediction=config["mags_orf_prediction"], allow_missing=True),
        mags_orfmap=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/simple_orf_contig_mapping.tsv", mags_orf_prediction=config["mags_orf_prediction"], allow_missing=True),
        mags_cov=expand("{wdir}/{sample}/{mags_coverage}/", mags_coverage=config["mags_coverage"], allow_missing=True),
    output:
        hmms_search="{wdir}/{sample}/mags_hmmsearch/{mag}/HMMs_coverage_table.tsv",
    params:
        hmm_folder=config["hmm_folder"],
        local_sample="{sample}",
        user_params= ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags_hmmsearch"])) ) (config["USER_PARAMS"]["mags_hmmsearch"]) 
    threads: config["threads"]
    run:

        output_folder = os.path.dirname(str(output.hmms_search))

        shell("mkdir -p {output_folder}")

        import pandas as pd
        df_mapping = pd.read_csv(str(input.mags_orfmap), sep="\t")

        coverage_methods = []
        with open(os.path.join(str(input.mags_cov), "list.txt")) as fd:
            for line in fd:
                coverage_methods.append(line.rstrip("\n"))

        list_output_files = []
        for hmm in os.listdir(params.hmm_folder):
            if not hmm.endswith('.hmm'):
                continue
            
            filename=hmm.split(".hmm")[0]
            out_path=os.path.join(output_folder, "output_hmms", filename)
            shell("mkdir -p {out_path}")

            hmm_file=os.path.join(params.hmm_folder, hmm)
            shell("hmmsearch --tblout /dev/null -o {out_path}/hmmsearch_output.txt {params.user_params} --cpu {threads} --notextw {hmm_file} {input.mags_orf}") 
            if os.stat(os.path.join(out_path, "hmmsearch_output.txt")).st_size == 0:
                continue

            list_output_files.append(str(os.path.join(out_path, "hmmsearch_output.txt")))

        from geomosaic.parser.make_hmmsearch_dataframe import make_hmmsearch_dataframe
        df_hmmresults = make_hmmsearch_dataframe(list_output_files, mags=True)
        df_hmmresults.drop_duplicates(inplace=True)
        df_hmmresults.to_csv(os.path.join(output_folder, "hmmsearch_results.tsv"), sep="\t", header=True, index=False)

        m1 = df_hmmresults.merge(df_mapping, on="orf_id", how="left")

        for mtd in coverage_methods:
            df_coverage = pd.read_csv(os.path.join(str(input.coverage_folder), f"{mtd}.tsv"), sep="\t")
            df_coverage.columns = ['mags', mtd]
            temp = pd.merge(m1, df_coverage, how="left", on="mags")
            m1 = temp.copy()
        
        m1["sample"] = str(params.local_sample)

        m1.to_csv(os.path.join(output_folder, "HMMs_coverage_table.tsv"), sep="\t", header=True, index=False)

def get_magshmmsearch_inputs(f_string): 
    def _f(wildcards):
        import pandas as pd

        mags_file = checkpoints.gather_mags_prodigal_outputs.get(**wildcards).output.mags_file
        df_mags = pd.read_csv(mags_file, sep="\t")
        
        _temp = []
        for m in df_mags.MAGs:
            _temp.append(f_string.format(mag=m, **wildcards) )

        return _temp
    return _f

rule gather_mags_hmmsearch_inputs:
    input: get_magshmmsearch_inputs("{wdir}/{sample}/mags_hmmsearch/{mag}/HMMs_coverage_table.tsv")
    output: touch("{wdir}/{sample}/mags_hmmsearch/gather_OK.txt")
    threads: 1

