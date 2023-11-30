rule run_recognizer_db:
    output:
        directory("{wdir}/reCOGnizer_DB")
    params:
        download_resource="--download-resources"
    run:
        shell("mkdir -p {output}/null_results")
        shell("(cd {output} & recognizer --resources-directory {output} {params.download_resource} --output {output}/null_results)")

rule run_recognizer:
    input:
        orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["orf_prediction"], allow_missing=True),
        recognizer_db={rules.run_recognizer_db.output}
    output:
        recognizer_result="{wdir}/{sample}/recognizer/reCOGnizer_results.tsv",
    conda: config["ENVS"]["recognizer"]
    params:
        user_params= ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["recognizer"])) ) (config["USER_PARAMS"]["recognizer"]) 
    threads: 5
    shell:
        """
        recognizer_folder=$(dirname {output.recognizer_result})

        mkdir -p $recognizer_folder

        (cd $recognizer_folder & recognizer \
                --file {input.orf_predicted} \
                --output $recognizer_folder \
                --resources-directory {input.recognizer_db} \
                {params.user_params} \
                --threads {threads})
        """
