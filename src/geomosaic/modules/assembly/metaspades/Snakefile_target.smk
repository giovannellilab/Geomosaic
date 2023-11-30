
rule all_metaspades:
    input:
        expand("{wdir}/{sample}/metaspades/geomosaic_contigs.fasta", sample=config["SAMPLES"], wdir=config["WDIR"])
        expand("{wdir}/{sample}/metaspades/mapping.tsv", sample=config["SAMPLES"], wdir=config["WDIR"])