
rule run_bakta:
    input:
        gm_contigs=expand(
            "{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta",
            assembly=config["MODULES"]["assembly"],
            allow_missing=True
        ),
        db_folder=expand(
            "{bakta_extdb_folder}/db",
            bakta_extdb_folder=config["EXT_DB"]["bakta"]
        )
    output:
        folder=directory("{wdir}/{sample}/bakta"),
        annotation="{wdir}/{sample}/bakta/bakta_annotation.tsv"
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
        mkdir -p {output.folder}

        bakta \
            --db {input.db_folder} \
            --output {output.folder} \
            --prefix bakta_annotation \
            --threads {threads} \
            --force \
            {input.gm_contigs}
        """
