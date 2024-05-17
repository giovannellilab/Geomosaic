
rule gtdbtk_db:
    params:
        gtdbk_url="https://data.ace.uq.edu.au/public/gtdb/data/releases/latest/auxillary_files/gtdbtk_package/full_package/gtdbtk_data.tar.gz",
        filename="gtdbtk_r220_data.tar.gz"
    output:
        directory(expand("{gtdbtk_extdb_folder}", gtdbtk_extdb_folder=config["EXT_DB"]["mags_gtdbtk"]))
    message: "GEOMOSAIC MSG: Starting to setup the database for GTDBTk"
    threads: 1
    run:
        shell("mkdir -p {output}")
        shell("curl --silent {params.gtdbk_url} -o {output}/{params.filename}")
        shell("tar -xzf {output}/{params.filename} --directory {output}")
