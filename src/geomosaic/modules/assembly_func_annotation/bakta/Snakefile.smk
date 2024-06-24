
rule run_bakta:
    input:
        gm_contigs=expand(
            "{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta",
            assembly=config["MODULES"]["assembly"],
            allow_missing=True
        ),
        db_folder=expand(
            "{bakta_extdb_folder}",
            bakta_extdb_folder=config["EXT_DB"]["bakta"]
        )
    output:
        folder=directory("{wdir}/{sample}/bakta")
        file_prefix="bakta_annotation"
    threads: config["threads"]
    conda: config["ENVS"]["bakta"]
    params:
        user_params=(
            lambda x: " ".join(
                filter(None, yaml.safe_load(open(x, "r"))["bakta"])
            )
        )(config["USER_PARAMS"]["bakta"])
    shell:
        """
        bakta \
            --db {input.db_folder} \
            --prefix {output.folder}/{output.file_prefix} \
            --threads {threads} \
            {input.gm_contigs}
        """
