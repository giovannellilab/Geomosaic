
rule all_kaiju:
    input: 
        expand("{wdir}/{sample}/kaiju/kaiju.out", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/kaiju", sample=config["SAMPLES"], wdir=config["WDIR"]),
