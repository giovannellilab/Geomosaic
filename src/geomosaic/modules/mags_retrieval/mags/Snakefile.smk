
rule run_mags:
    input:
        dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["binning_derep"], allow_missing=True),
        checkm_folder=expand("{wdir}/{sample}/{binning_qa}", binning_qa=config["binning_qa"], allow_missing=True)
    output:
        directory("{wdir}/{sample}/mags")
    params:
        completness_threshold=config["completness_threshold"],
        contamination_threshold=config["contamination_threshold"],
    run:
        shell("mkdir -p {output}/fasta")

        from geomosaic.parsing_output.retrieve_survival_mags import retrieve_survival_mags

        checkm_table = os.path.join(str(input.checkm_folder), "checkm_output.tsv")
        das_tool_bins = os.path.join(str(input.dins_derep), "bins")
        mags_outfolder = str(output)

        retrieve_survival_mags(checkm_table, das_tool_bins, params.completness_threshold, params.contamination_threshold, mags_outfolder)
