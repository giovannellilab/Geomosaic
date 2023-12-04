
rule run_quast:
    input:
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/quast")
    threads: config["threads"]
    conda: config["ENVS"]["quast"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["quast"])) ) (config["USER_PARAMS"]["quast"]) 
    shell:
        """
        quast {params.user_params} --threads {threads} -o {output} {input.gm_contigs}
        """
