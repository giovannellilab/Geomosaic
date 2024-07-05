
rule checkm_db:
    params:
        db_link="https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz"    
    output:
        db_folder=directory(expand("{checkm_extdb_folder}", checkm_extdb_folder=config["EXT_DB"]["checkm"])),
    conda: config["ENVS_EXTDB"]["checkm"]
    message: "GEOMOSAIC MSG: Starting to setup the database for CheckM"
    threads: 1
    shell:
        """
        mkdir -p {output.db_folder}
        (cd {output.db_folder} && wget --quiet {params.db_link} && tar -x -f *.tar.gz)
        checkm data setRoot {output.db_folder}
        """
