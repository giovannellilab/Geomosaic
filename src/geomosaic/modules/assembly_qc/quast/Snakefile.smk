
rule run_quast:
    input:
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/quast")
    threads: 5
    params:
        extra="--contig-thresholds 0,1000,10000,100000,1000000",
        label="--labels metaspades"
    run:
        shell("quast --threads {threads} {params.extra} -o {output} {input.contig_path}/contigs.fasta")
