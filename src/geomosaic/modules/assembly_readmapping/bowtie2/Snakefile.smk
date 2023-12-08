
rule run_bowtie2:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/bowtie2"),
        sam_file="{wdir}/{sample}/bowtie2/read_mapping.sam",
        bam_file="{wdir}/{sample}/bowtie2/read_mapping.bam",
        sorted_bam="{wdir}/{sample}/bowtie2/read_mapping_sorted.bam",
        indexed_bam="{wdir}/{sample}/bowtie2/read_mapping_sorted.bam.bai"
    threads: config["threads"]
    conda: config["ENVS"]["bowtie2"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["bowtie2"])) ) (config["USER_PARAMS"]["bowtie2"]) 
    shell:
        """mkdir -p {output.folder}/b_index

        bowtie2-build --quiet --threads {threads} {input.gm_contigs} {output.folder}/b_index/gmindex
        
        bowtie2 {params.user_params} \
            --threads {threads} \
            --sensitive \
            -x {output.folder}/b_index/gmindex \
            -1 {input.r1} \
            -2 {input.r2} \
            -S {output.sam_file}
        
        samtools view -@ {threads} -S -b {output.sam_file} > {output.bam_file}

        samtools sort -@ {threads} {output.bam_file} -o {output.sorted_bam}

        samtools index -@ {threads} {output.sorted_bam} {output.indexed_bam}
        """