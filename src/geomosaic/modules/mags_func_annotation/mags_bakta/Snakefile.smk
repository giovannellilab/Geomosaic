
rule run_mags_bakta:
    input:
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True),
        db_folder=expand("{mags_bakta_extdb_folder}/db", mags_bakta_extdb_folder=config["EXT_DB"]["mags_bakta"])
    output:
        folder=directory("{wdir}/{sample}/mags_bakta"),
        annotation="{wdir}/{sample}/mags_bakta/bakta_annotation.tsv"
    threads: config["threads"]
    conda: config["ENVS"]["mags_bakta"]
    params:
        user_params=(lambda x: " ".join(filter(None, yaml.safe_load(open(x, "r"))["mags_bakta"])))(config["USER_PARAMS"]["mags_bakta"])
    shell:
        """
        mkdir -p {output.folder}

        bakta \
            --db {input.db_folder} \
            --output {output.folder} \
            --prefix bakta_annotation \
            --threads {threads} \
            --force \
            {input.gm_contigs}
        """
