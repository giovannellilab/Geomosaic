rule funcprofiler_db:
    params:
        db='wget https://zenodo.org/records/10045253/files/KOs_sketched_scaled_1000.sig.zip"
        filename=
    output:
        directory(expand("{funcprofiler_extdb_folder}")), funcprofiler_extdb_folder=config["EXT_DB"]["funcprofiler"]
    message: "GEOMOSAIC MSG: Starting to setup the database for funcprofiler"
    threads: 1
    shell:
    """
    mkdir -p {output}
    (cd {output} && )
    curl --silent --output {output}/{params.filename}
    """
