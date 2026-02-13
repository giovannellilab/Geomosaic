
rule all_rmi_rpi_indexes:
    input:
        expand("{wdir}/{sample}/rmi_rpi_indexes", sample=config["SAMPLES"], wdir=config["WDIR"]),
