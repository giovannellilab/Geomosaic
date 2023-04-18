
rule run_metagahit:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/megahit")
    threads: 10
    params:
        complex_metagenome="--presets meta-large"
    run:
        shell("megahit {params.complex_metagenome} -t {threads} --memory 0.7 -1 {input.r1} -2 {input.r2} -o {output}")
        shell("mv {output}/final.contigs.fa {output}/contigs.fasta")
