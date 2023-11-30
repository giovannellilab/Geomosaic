
rule run_das_tool:
    input:
        concoct_bins=expand("{wdir}/{sample}/{binning}/concoct/bins", binning=config["binning"], allow_missing=True),
        maxbin_bins=expand("{wdir}/{sample}/{binning}/maxbin2/bins", binning=config["binning"], allow_missing=True),
        metabat_bins=expand("{wdir}/{sample}/{binning}/metabat2/bins", binning=config["binning"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/das_tool")
    threads: 5
    conda: config["ENVS"]["das_tool"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["das_tool"])) ) (config["USER_PARAMS"]["das_tool"]) 
    log: "{wdir}/{sample}/benchmark/das_tool.log"
    shell:
        """
        mkdir -p {output.folder}

        Fasta_to_Contig2Bin.sh -i {input.concoct_bins} -e fasta > {output.folder}/concoct_dastool.tsv
        Fasta_to_Contig2Bin.sh -i {input.maxbin_bins} -e fasta > {output.folder}/maxbin2_dastool.tsv
        Fasta_to_Contig2Bin.sh -i {input.metabat_bins} -e fasta > {output.folder}/metabat2_dastool.tsv

        DAS_Tool -i {output.folder}/concoct_dastool.tsv,{output.folder}/maxbin2_dastool.tsv,{output.folder}/metabat2_dastool.tsv \
            -l concoct,maxbin2,metabat2 \
            -c {input.gm_contigs} \
            -o {output.folder}/das_tool \
            --threads {threads} \
            {params.user_params}
        
        (cd {output.folder} && mv das_tool_DASTool_bins bins)
        """
