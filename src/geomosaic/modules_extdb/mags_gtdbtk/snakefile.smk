
rule gtdbtk_db:
    params:
        gtdbk_url="https://data.gtdb.ecogenomic.org/releases/release207/207.0/auxillary_files/gtdbtk_r207_v2_data.tar.gz"
    output:
        directory(expand("{gtdbtk_extdb_folder}", gtdbtk_extdb_folder=config["EXT_DB"]["mags_gtdbtk"]))
    message: "GEOMOSAIC MSG: Starting to setup the database for GTDBTk"
    run:
        shell("mkdir -p {output}")
        shell("wget {params.gtdbk_url} -O {output}/gtdbtk_r207_v2_data.tar.gz")
        shell("tar -xzvf {output}/gtdbtk_r207_v2_data.tar.gz --directory {output}")
