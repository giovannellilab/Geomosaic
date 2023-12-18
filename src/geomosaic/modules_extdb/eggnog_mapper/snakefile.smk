
rule eggnog_mapper_db:
    output:
        directory(expand("{eggnog_mapper_extdb_folder}", eggnog_mapper_extdb_folder=config["EXT_DB"]["eggnog_mapper"]))
    conda: config["ENVS"]["eggnog_mapper"]
    message: "GEOMOSAIC MSG: Starting to setup the database for eggNOG Mapper"
    threads: 1
    shell:
        """
        mkdir -p {output}

        download_eggnog_data.py -y -q --data_dir {output}
        """
