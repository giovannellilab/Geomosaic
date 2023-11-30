
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

rule gtdbtk_classify:
    input:
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["mags_retrieval"], allow_missing=True),
        db=rules.download_gtdbtk.output
    output:
        directory("{wdir}/{sample}/mags_gtdbtk")
    params:
        extension="fa",
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags_gtdbtk"])) ) (config["USER_PARAMS"]["mags_gtdbtk"]) 
    benchmark: "{wdir}/benchmark/{sample}_gtdbtk.txt"
    threads: 20
    conda: config["ENVS"]["mags_gtdbtk"]
    shell:
        """
        mkdir -p {output}

        GTDBTK_DATA_PATH={input.db}/release207_v2 gtdbtk classify_wf \
            --genome_dir {input.mags_folder}/fasta \
            --out_dir {output} \
            --cpus {threads} \
            --mash_db {input.db}/mash_db_gtdbtk_r207_vs.msh \
            --extension {params.extension}
        """
