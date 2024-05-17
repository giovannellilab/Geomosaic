
rule run_recognizer:
    input:
        orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True),
        recognizer_db=expand("{recognizer_extdb_folder}", recognizer_extdb_folder = config["EXT_DB"]["recognizer"])
    output:
        recognizer_result="{wdir}/{sample}/recognizer/reCOGnizer_results.tsv",
    conda: config["ENVS"]["recognizer"]
    params:
        user_params= ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["recognizer"])) ) (config["USER_PARAMS"]["recognizer"]) 
    threads: config["threads"]
    shell:
        """
        recognizer_folder=$(dirname {output.recognizer_result})

        mkdir -p $recognizer_folder

        (cd $recognizer_folder && recognizer \
                --file {input.orf_predicted} \
                --output $recognizer_folder \
                --resources-directory {input.recognizer_db} \
                {params.user_params} \
                --threads {threads})
        """
