
rule run_mifaser:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        mifaser_db=expand("{mifaser_extdb_folder}", mifaser_extdb_folder=config["EXT_DB"]["mifaser"]),
    output:
        directory("{wdir}/{sample}/mifaser")
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mifaser"])) ) (config["USER_PARAMS"]["mifaser"]),
    conda: config["ENVS"]["mifaser"]
    threads: config["threads"]
    shell:
        """
        mifaser {params.user_params} -d {input.mifaser_db}/GS-21-all -l {input.r1} {input.r2} -t {threads} -o {output}
        """
