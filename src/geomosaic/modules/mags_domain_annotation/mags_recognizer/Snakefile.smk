
rule run_mags_recognizer:
    input:
        mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/orf_predicted.faa", mags_orf_prediction=config["mags_orf_prediction"], allow_missing=True),
        recognizer_db={rules.run_recognizer_db.output}
    output:
        recognizer_result="{wdir}/{sample}/mags_recognizer/{mag}/reCOGnizer_results.tsv",
    conda: config["ENVS"]["mags_recognizer"]
    params:
        user_params= ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags_recognizer"])) ) (config["USER_PARAMS"]["mags_recognizer"]) 
    threads: 5
    shell:
        """
        recognizer_folder=$(dirname {output.recognizer_result})

        mkdir -p $recognizer_folder

        (cd $recognizer_folder & recognizer \
                --file {input.mags_orf} \
                --output $recognizer_folder \
                --resources-directory {input.recognizer_db} \
                {params.user_params} \
                --threads {threads})
        """

def get_recognizer_inputs(f_string): 
    def _f(wildcards):
        import pandas as pd

        mags_file = checkpoints.gather_mags_prodigal_outputs.get(**wildcards).output.mags_file
        df_mags = pd.read_csv(mags_file, sep="\t")
        
        _temp = []
        for m in df_mags.MAGs:
            _temp.append(f_string.format(mag=m, **wildcards) )

        return _temp
    return _f

rule gather_mags_recognizer_inputs:
    input: get_recognizer_inputs("{wdir}/{sample}/mags_recognizer/{mag}/reCOGnizer_results.tsv")
    output: touch("{wdir}/{sample}/mags_recognizer/gather_OK.txt")
    threads: 1

