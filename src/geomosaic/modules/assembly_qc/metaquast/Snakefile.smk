
rule run_metaquast:
    input:
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/metaquast")
    threads: config["threads"]
    conda: config["ENVS"]["metaquast"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["quast"])) ) (config["USER_PARAMS"]["metaquast"]) 
    shell:
        """
        quast --meta {params.user_params} --threads {threads} -o {output} {input.gm_contigs}
        """
