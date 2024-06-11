
rule all_mags_bakta:
    input: 
        expand(
            "{wdir}/{sample}/mags_bakta",
            sample=config["SAMPLES"],
            wdir=config["WDIR"]
        ),
