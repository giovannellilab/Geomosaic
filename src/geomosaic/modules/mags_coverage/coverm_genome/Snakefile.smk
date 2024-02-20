
rule run_coverm_genome:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True),
    output:
        folder=directory("{wdir}/{sample}/coverm_genome"),
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["coverm_genome"])) ) (config["USER_PARAMS"]["coverm_genome"]) 
    threads: config["threads"]
    conda: config["ENVS"]["coverm_genome"]
    shell:
        """
        mkdir -p {output.folder}/tmp

        touch {output.folder}/list.txt

        for mtd in relative_abundance mean trimmed_mean tpm; do
            TMPDIR={output.folder}/tmp coverm genome --coupled {input.r1} {input.r2} \
                --genome-fasta-directory {input.mags_folder}/fasta \
                --genome-fasta-extension fa \
                --output-file {output.folder}/$mtd.tsv \
                --threads {threads} \
                --methods $mtd \
            {params.user_params}

            echo $mtd >> {output.folder}/list.txt
        done;

        (cd {output.folder} && rm -r tmp)
        """