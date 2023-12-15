
rule kraken2_db:
    params:
        db_link="https://genome-idx.s3.amazonaws.com/kraken/k2_standard_20231009.tar.gz"
    output:
        db_folder=directory(expand("{kraken2_extdb_folder}", kraken2_extdb_folder=config["EXT_DB"]["kraken2"])),
    message: "GEOMOSAIC MSG: Starting to setup the database for kraken2"
    shell:
        """
        mkdir -p {output.db_folder}
        (cd {output.db_folder} && wget --quiet {params.db_link} && tar -x -f *.tar.gz)
        (cd {output.db_folder} && rm *.tar.gz)
        """
