
rule run_coverm:
    input:
        sorted_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
        indexed_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam.bai", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
    output:
        folder=directory("{wdir}/{sample}/coverm"),
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["coverm"])) ) (config["USER_PARAMS"]["coverm"]) 
    threads: config["threads"]
    conda: config["ENVS"]["coverm"]
    shell:
        """
        mkdir -p {output.folder}/tmp

        touch {output.folder}/list.txt

        for mtd in mean trimmed_mean count tpm; do
            TMPDIR={output.folder}/tmp coverm contig --bam-files {input.sorted_bam} \
                --output-file {output.folder}/$mtd.tsv \
                --threads {threads} \
                --methods $mtd \
                {params.user_params}
            
            echo $mtd >> {output.folder}/list.txt
        done;

        (cd {output.folder} && rm -r tmp)
        """