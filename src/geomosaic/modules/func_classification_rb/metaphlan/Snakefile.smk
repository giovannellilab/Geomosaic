
rule run_metaphlan:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/metaphlan")
    threads: 5
    run:
        shell("mkdir -p {output}")
        shell("metaphlan {input.r1},{input.r2} --bowtie2out {output}/metaphlan.bowtie2.bz2 --nproc {threads} --input_type fastq -o {output}/profiled_metagenome.txt")
        shell("metaphlan -t marker_pres_table {output}/metaphlan.bowtie2.bz2 --input_type bowtie2out -o {output}/marker_abundance_table.txt")
        shell("metaphlan -t rel_ab_w_read_stats {output}/metaphlan.bowtie2.bz2 --input_type bowtie2out -o {output}/profile_and_estimation.txt")
