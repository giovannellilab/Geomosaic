rule run_funcprofiler:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        funcprofiler_db=expand("{funcprofiler_extdb_folder}", funcprofiler_extdb_folder=config["EXT_DB"]["funcprofiler"]),
    output:
        folder = directory("{wdir}/{sample}/funcprofiler")
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["funcprofiler"])) ) (config["USER_PARAMS"]["funcprofiler"]),
    conda: config["ENVS"]["funcprofiler"]
    threads: config["threads"]
    shell:
        """
        mkdir -p {output.folder}

        echo "[+] Concatenating reads ..."
        seq_file={output.folder}/seq_concat.gz
        zcat {input.r1} {input.r2} > seq_file.fastq.gz
        echo "[+] Reads successfully concatenated into {seq_file}"

        python {fun_dir}/funcprofiler.py seq_file {fun_dir}/KOs_sketched_scaled_500.sig.zip {params.user_params} ko_profiles.csv -t {threads} -p prefetch_out.txt

        echo "[+] Removing concatenated reads ..."
        rm seq_file
        echo "[SUCCESS] funprofiler job finished for {sample}

        """