
rule all_mags_recognizer:
    input:
        expand("{wdir}/{sample}/mags_recognizer/gather_OK.txt", sample=config["SAMPLES"], wdir=config["WDIR"]),
