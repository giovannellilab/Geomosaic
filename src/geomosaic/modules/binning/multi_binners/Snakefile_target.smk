
rule all_multi_binners:
    input:
        expand("{wdir}/{sample}/multi_binners/geomosaic_concoct_bins", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/multi_binners/geomosaic_maxbin2_bins", sample=config["SAMPLES"], wdir=config["WDIR"]),
        expand("{wdir}/{sample}/multi_binners/geomosaic_metabat2_bins", sample=config["SAMPLES"], wdir=config["WDIR"]),
