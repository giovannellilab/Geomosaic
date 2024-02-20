
rule gtdbtk_classify:
    input:
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True),
        db=expand("{gtdbtk_extdb_folder}", gtdbtk_extdb_folder=config["EXT_DB"]["mags_gtdbtk"])
    output:
        directory("{wdir}/{sample}/mags_gtdbtk")
    params:
        extension="fa",
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags_gtdbtk"])) ) (config["USER_PARAMS"]["mags_gtdbtk"])
    threads: config["threads"]
    conda: config["ENVS"]["mags_gtdbtk"]
    log: "{wdir}/{sample}/mags_gtdbtk/gm_log.out"
    shell:
        """
        mkdir -p {output}

        GTDBTK_DATA_PATH={input.db}/release207_v2 gtdbtk classify_wf \
            --genome_dir {input.mags_folder}/fasta \
            --out_dir {output} \
            --cpus {threads} \
            --mash_db {input.db}/mash_db_gtdbtk_r207_vs.msh \
            --extension {params.extension} >> {log} 2>&1
        """
