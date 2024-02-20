
rule run_das_tool:
    input:
        concoct_bins=expand("{wdir}/{sample}/{binning}/geomosaic_concoct_bins", binning=config["MODULES"]["binning"], allow_missing=True),
        maxbin_bins=expand("{wdir}/{sample}/{binning}/geomosaic_maxbin2_bins", binning=config["MODULES"]["binning"], allow_missing=True),
        metabat_bins=expand("{wdir}/{sample}/{binning}/geomosaic_metabat2_bins", binning=config["MODULES"]["binning"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/das_tool")
    threads: config["threads"]
    conda: config["ENVS"]["das_tool"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["das_tool"])) ) (config["USER_PARAMS"]["das_tool"]),
        write_bins_evals = "--write_bin_evals",
        write_bins = "--write_bins"
    log: "{wdir}/{sample}/das_tool/gm_log.out"
    shell:
        """
        mkdir -p {output.folder}

        LC_ALL=C Fasta_to_Contig2Bin.sh -i {input.concoct_bins} -e fasta > {output.folder}/concoct_dastool.tsv
        LC_ALL=C Fasta_to_Contig2Bin.sh -i {input.maxbin_bins} -e fasta > {output.folder}/maxbin2_dastool.tsv
        LC_ALL=C Fasta_to_Contig2Bin.sh -i {input.metabat_bins} -e fasta > {output.folder}/metabat2_dastool.tsv

        LC_ALL=C DAS_Tool -i {output.folder}/concoct_dastool.tsv,{output.folder}/maxbin2_dastool.tsv,{output.folder}/metabat2_dastool.tsv \
            -l concoct,maxbin2,metabat2 \
            -c {input.gm_contigs} \
            -o {output.folder}/das_tool \
            --threads {threads} \
            {params.write_bins} \
            {params.write_bins_evals} \
            {params.user_params} >> {log} 2>&1
        
        (cd {output.folder} && mv das_tool_DASTool_bins bins)
        """
