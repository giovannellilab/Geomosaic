
rule all_mags_recognizer:
    input:
        expand("{wdir}/{sample}/mags_recognizer", sample=config["SAMPLES"], wdir=config["WDIR"]),
