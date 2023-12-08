
rule run_coverm:
    input:
        folder_readmap=expand("{wdir}/{sample}/{assembly_readmapping}", assembly_readmapping=config["assembly_readmapping"], allow_missing=True),
    output:
        folder=directory("{wdir}/{sample}/coverm"),
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["coverm"])) ) (config["USER_PARAMS"]["coverm"]) 
    threads: config["threads"]
    conda: config["ENVS"]["coverm"]
    shell:
        """
        mkdir -p {output.folder}

        for mtd in mean trimmed_mean count tpm; do
            coverm contig --bam-files {input.folder_readmap}/read_mapping_sorted.bam \
                --output-file {output.folder}/$mtd.tsv \
                --threads {threads} \
                --methods $mtd \
                {params.user_params}
        done;
        """
