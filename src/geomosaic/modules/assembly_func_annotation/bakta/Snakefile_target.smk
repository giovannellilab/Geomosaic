
rule all_assembly_bakta:
    input: 
        expand(
            "{wdir}/{sample}/bakta",
            sample=config["SAMPLES"],
            wdir=config["WDIR"]
        ),
