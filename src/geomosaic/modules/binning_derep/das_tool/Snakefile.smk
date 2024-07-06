
rule run_das_tool:
    input:
        multi_binners_folder=expand("{wdir}/{sample}/{binning}", binning=config["MODULES"]["binning"], allow_missing=True),
        semibin_bins=expand("{wdir}/{sample}/{binning}/geomosaic_semibin2_bins", binning=config["MODULES"]["binning"], allow_missing=True),
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
    shell:
        """
        mkdir -p {output.folder}

        DT_labels=""
        DT_inputs=""

        if [ -f {input.multi_binners_folder}/semibin2_ok.out ]; then
            LC_ALL=C Fasta_to_Contig2Bin.sh -i {input.semibin_bins} -e fasta > {output.folder}/semibin2_dastool.tsv
            DT_labels="semibin2",$DT_labels
            DT_inputs={output.folder}/semibin2_dastool.tsv,$DT_inputs
        fi

        if [ -f {input.multi_binners_folder}/maxbin2_ok.out ]; then
            LC_ALL=C Fasta_to_Contig2Bin.sh -i {input.maxbin_bins} -e fasta > {output.folder}/maxbin2_dastool.tsv
            DT_labels="maxbin2",$DT_labels
            DT_inputs={output.folder}/maxbin2_dastool.tsv,$DT_inputs
        fi

        if [ -f {input.multi_binners_folder}/metabat2_ok.out ]; then
            LC_ALL=C Fasta_to_Contig2Bin.sh -i {input.metabat_bins} -e fasta > {output.folder}/metabat2_dastool.tsv
            DT_labels="metabat2",$DT_labels
            DT_inputs={output.folder}/metabat2_dastool.tsv,$DT_inputs
        fi

        DT_labels=$(echo $DT_labels |sed 's/,$//')
        DT_inputs=$(echo $DT_inputs |sed 's/,$//')

        LC_ALL=C DAS_Tool -i $DT_inputs \
            -l $DT_labels \
            -c {input.gm_contigs} \
            -o {output.folder}/das_tool \
            --threads {threads} \
            {params.write_bins} \
            {params.write_bins_evals} \
            {params.user_params}
        
        (cd {output.folder} && mv das_tool_DASTool_bins bins)
        """
