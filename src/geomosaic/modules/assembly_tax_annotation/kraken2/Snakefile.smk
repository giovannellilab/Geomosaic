
rule run_kraken2:
    input:
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True),
        db_folder=expand("{kraken2_extdb_folder}", kraken2_extdb_folder=config["EXT_DB"]["kraken2"])
    output:
        directory("{wdir}/{sample}/kraken2")
    threads: config["threads"]
    conda: config["ENVS"]["kraken2"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["kraken2"])) ) (config["USER_PARAMS"]["kraken2"]) 
    shell:
        """
        mkdir -p {output}

        LC_ALL=C kraken2 \
            --db {input.db_folder} \
            --threads {threads} \
            --use-names \
            --output {output}/kraken_output.txt \
            --report {output}/kraken_report.txt \
            --report-zero-counts \
            {input.gm_contigs}
        """
