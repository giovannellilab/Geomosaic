
rule all_megahit:
    input:
        expand("{wdir}/{sample}/megahit/geomosaic_contigs.fasta", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/megahit/mapping.tsv", sample=config["SAMPLES"], wdir=config["WDIR"]),
