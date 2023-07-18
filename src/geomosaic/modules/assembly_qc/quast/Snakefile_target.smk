
rule all_quast:
    input:
        expand("{wdir}/{sample}/quast", sample=config["SAMPLES"], wdir=config["WDIR"]),
