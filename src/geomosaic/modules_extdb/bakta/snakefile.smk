
rule bakta_db:
    output:
        directory(expand("{bakta_extdb_folder}", bakta_extdb_folder=config["EXT_DB"]["bakta"]))
    conda: config["ENVS"]["bakta"]
    message: "GEOMOSAIC MSG: Starting to setup the database for bakta"
    threads: 1
    shell:
        """
        mkdir -p {output}

        bakta_db download --output {output} --type 'full'
        """
