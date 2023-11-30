
rule download_gtdbtk:
    params:
        gtdbk_url="https://data.gtdb.ecogenomic.org/releases/release207/207.0/auxillary_files/gtdbtk_r207_v2_data.tar.gz"
    output:
        directory("/mnt/data/bigdata/gtdbtk_db")
    run:
        shell("echo 'A'")
        # shell("mkdir -p {output}")
        # shell("wget {params.gtdbk_url} -O {output}/gtdbtk_r207_v2_data.tar.gz")
        # shell("tar -xzvf {output}/gtdbtk_r207_v2_data.tar.gz --directory {output}")
