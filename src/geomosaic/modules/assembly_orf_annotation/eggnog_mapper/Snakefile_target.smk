
rule all_eggnog_mapper:
    input:
        expand("{wdir}/{sample}/eggnog_mapper", sample=config["SAMPLES"], wdir=config["WDIR"]),
