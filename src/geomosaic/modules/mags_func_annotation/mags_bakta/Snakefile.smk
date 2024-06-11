
rule run_mags_bakta:
    input:
        mags_folder=expand(
            "{wdir}/{sample}/{mags_retrieval}",
            mags_retrieval=config["MODULES"]["mags_retrieval"],
            allow_missing=True
        ),
        db_folder=expand(
            "{bakta_extdb_folder}",
            bakta_extdb_folder=config["EXT_DB"]["bakta"]
        )
    output:
        file_prefix="bakta_annotation"
    threads: config["threads"]
    conda: config["ENVS"]["bakta"]
    params:
        user_params=(
            lambda x: " ".join(
                filter(None, yaml.safe_load(open(x, "r"))["mags_bakta"])
            )
        )(config["USER_PARAMS"]["mags_bakta"])
    shell:
        """
        bakta \
            --db {input.db_folder} \
            --prefix {output.file_prefix} \
            --threads {threads}
            {input.mags_folder}
        """
