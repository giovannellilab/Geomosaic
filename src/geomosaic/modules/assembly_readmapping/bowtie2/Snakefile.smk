
rule run_bowtie2:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/bowtie2"),
        sam_file=temp("{wdir}/{sample}/bowtie2/read_mapping.sam"),
        bam_file=temp("{wdir}/{sample}/bowtie2/read_mapping.bam"),
        sorted_bam="{wdir}/{sample}/bowtie2/read_mapping_sorted.bam",
        indexed_bam="{wdir}/{sample}/bowtie2/read_mapping_sorted.bam.bai"
    threads: config["threads"]
    conda: config["ENVS"]["bowtie2"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["bowtie2"])) ) (config["USER_PARAMS"]["bowtie2"]),
        samtools_view_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["samtools_view"])) ) (config["USER_PARAMS"]["bowtie2"]),
        samtools_sort_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["samtools_sort"])) ) (config["USER_PARAMS"]["bowtie2"]),
        samtools_index_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["samtools_index"])) ) (config["USER_PARAMS"]["bowtie2"])
    shell:
        """mkdir -p {output.folder}/b_index

        bowtie2-build --quiet --threads {threads} {input.gm_contigs} {output.folder}/b_index/gmindex
        
        bowtie2 {params.user_params} \
            --threads {threads} \
            -x {output.folder}/b_index/gmindex \
            -1 {input.r1} \
            -2 {input.r2} \
            -S {output.sam_file}
        
        samtools view -@ {threads} {params.samtools_view_user_params} -S -b {output.sam_file} > {output.bam_file}

        samtools sort -@ {threads} {params.samtools_sort_user_params} {output.bam_file} -o {output.sorted_bam}

        samtools index -@ {threads} {params.samtools_index_user_params} {output.sorted_bam} {output.indexed_bam}
        """
