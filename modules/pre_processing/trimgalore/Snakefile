
rule run_trimgalore:
    input:
        r1="{wdir}/{sample}/R1.fastq.gz",
        r2="{wdir}/{sample}/R2.fastq.gz",
    output:
        dir=directory("{wdir}/{sample}/trimgalore"),
        r1="{wdir}/{sample}/trimgalore/R1.fastq.gz", 
        r2="{wdir}/{sample}/trimgalore/R2.fastq.gz"
    threads: 5
    params:
        extra="--paired --fastqc --gzip"
    run:
        shell("trim_galore {params.extra} --cores {threads} -o {output.dir} {input.r1} {input.r2}")
        shell("mv {output.dir}/R1_val_1.fq.gz {output.r1}")
        shell("mv {output.dir}/R2_val_2.fq.gz {output.r2}")
