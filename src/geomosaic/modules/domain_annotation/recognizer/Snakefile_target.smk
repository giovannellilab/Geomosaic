
rule all_recognizer:
    input:
        expand("{wdir}/{sample}/recognizer/reCOGnizer_results.tsv", sample=config["SAMPLES"], wdir=config["WDIR"]),
