
rule funcprofiler_db:
    params:
        db='https://zenodo.org/records/10045253/files/KOs_sketched_scaled_1000.sig.zip",
        filename="KOs_sketched_scaled_1000.sig.zip"
    output:
        directory(expand("{funcprofiler_extdb_folder}", funcprofiler_extdb_folder=config["EXT_DB"]["funcprofiler"]))
    message: "GEOMOSAIC MSG: Starting to setup the database for Funcprofiler"
    threads: 1
    shell:
        """
        mkdir -p {output}
        curl --silent --output {output}/{params.filename} {params.db}
        """

