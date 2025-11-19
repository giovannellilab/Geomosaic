
rule run_funprofiler:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        db_folder=expand("{funprofiler_extdb_folder}", funprofiler_extdb_folder=config["EXT_DB"]["funprofiler"]),
    output:
        directory("{wdir}/{sample}/funprofiler")
    conda: config["ENVS"]["funprofiler"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["funprofiler"])) ) (config["USER_PARAMS"]["funprofiler"]),
    threads: config["threads"]
    shell:
        """
        mkdir -p {output}

        echo "[+] Concatenating reads for sample: {wildcards.sample} "
        seq_file="{output}/seq_concat.fastq.gz"

        cat {input.r1} {input.r2} > $seq_file
        echo "[+] Reads successfully concatenated into $seq_file " 

        funprofiler $seq_file {input.db_folder}/KOs_sketched_scaled_1000.sig.zip {params.user_params} {output}/ko_profiles.csv -t {threads} -p {output}/prefetch_out.csv

        echo "[+] Removing concatenated reads ..."
        ( cd {output} && rm seq_concat.fastq.gz )
        echo "[SUCCESS] funprofiler job finished for {wildcards.sample} "
        """
