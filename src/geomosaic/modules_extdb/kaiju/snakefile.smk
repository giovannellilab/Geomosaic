
rule kaiju_db:
    params: 
        db="https://kaiju-idx.s3.eu-central-1.amazonaws.com/2023/kaiju_db_nr_2023-05-10.tgz",
        filename="kaiju_db.tgz"
    output:
        directory(expand("{kaiju_extdb_folder}", kaiju_extdb_folder=config["EXT_DB"]["kaiju"]))
    message: "GEOMOSAIC MSG: Starting to setup the database for Kaiju"
    threads: 1
    shell:
        """
        mkdir -p {output}
        curl --silent --output {output}/{params.filename} {params.db}
        (cd {output} && tar --extract --file={params.filename} && mv kaiju_db_*.fmi kaiju_db.fmi && rm {params.filename})
        """
