
rule checkm2_db:
    output:
        db_folder=directory(expand("{checkm2_extdb_folder}", checkm2_extdb_folder=config["EXT_DB"]["checkm2"])),
    conda: config["ENVS_EXTDB"]["checkm2"]
    message: "GEOMOSAIC MSG: Starting to setup the database for CheckM2"
    threads: 1
    shell:
        """
        mkdir -p {output.db_folder}
        checkm2 database --download --path {output.db_folder}
        """