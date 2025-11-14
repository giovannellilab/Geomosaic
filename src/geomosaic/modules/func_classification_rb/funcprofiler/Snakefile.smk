rule run_funcprofiler:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        db_folder=expand("{funcprofiler_extdb_folder}", funcprofiler_extdb_folder=config["EXT_DB"]["funcprofiler"]),
    output:
        folder = directory("{wdir}/{sample}/funcprofiler"),
        prefetch_out = "{wdir}/{sample}/funcprofiler/prefetch_out.txt",
        ko_profiles = "{wdir}/{sample}/funcprofiler/ko_profiles.csv",
    conda: config["ENVS"]["funcprofiler"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["funcprofiler"])) ) (config["USER_PARAMS"]["funcprofiler"]),
    threads: config["threads"]
    shell:
        """
        mkdir -p {output.folder}

        echo "[+] Concatenating reads ..."
        seq_file={output.folder}/seq_concat.fastq.gz
        zcat {input.r1} {input.r2} > $seq_file
        echo "[+] Reads successfully concatenated into {seq_file}"

        funcprofiler seq_file {input.db_folder} {params.user_params} {output.ko_profiles} -t {threads} -p {output.prefetch_out}

        echo "[+] Removing concatenated reads ..."
        rm -f seq_file
        echo "[SUCCESS] funprofiler job finished for {sample}

        """