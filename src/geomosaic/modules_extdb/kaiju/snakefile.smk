
rule kaiju_db:
    params: 
        db="https://kaiju.binf.ku.dk/database/kaiju_db_viruses_2022-03-29.tgz",
        filename="kaiju_db.tgz"
    output:
        directory(expand("{kaiju_extdb_folder}", kaiju_extdb_folder=config["EXT_DB"]["kaiju"]))
    message: "GEOMOSAIC MSG: Starting to setup the database for Kaiju"
    shell:
        """
        mkdir -p {output}
        curl --output {output}/{params.filename} {params.db}
        (cd {output} && tar --extract --file={params.filename} && mv kaiju_db_*.fmi kaiju_db.fmi && rm {params.filename})
        """
