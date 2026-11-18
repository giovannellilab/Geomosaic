
rule run_checkm2:
    input:
        dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["MODULES"]["binning_derep"], allow_missing=True),
        db_file=expand("{checkm2_extdb_folder}/CheckM2_database/uniref100.KO.1.dmnd", checkm2_extdb_folder=config["EXT_DB"]["checkm2"])
    output:
        folder=directory("{wdir}/{sample}/checkm2"),
        report="{wdir}/{sample}/checkm2/quality_report.tsv"
    threads: config["threads"]
    conda: config["ENVS"]["checkm2"]
    log: "{wdir}/{sample}/checkm2/gm_log.out"
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["checkm2"])) ) (config["USER_PARAMS"]["checkm2"]),
        extension="fa",
    shell:
        """
        ulimit -u 10000
        echo "CHECKM2_PREDICT"
        checkm2 predict \
            --threads {threads} \
            --input {input.dins_derep}/bins \
            --extension {params.extension} \
            --database_path {input.db_file} \
            --output-directory {output.folder} \
            {params.user_params} \
            --force >> {log} 2>&1
        """