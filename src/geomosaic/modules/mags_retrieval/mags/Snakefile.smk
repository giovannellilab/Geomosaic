
checkpoint run_mags:
    input:
        dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["MODULES"]["binning_derep"], allow_missing=True),
        checkm_folder=expand("{wdir}/{sample}/{binning_qa}", binning_qa=config["MODULES"]["binning_qa"], allow_missing=True)
    output:
        folder = directory("{wdir}/{sample}/mags"),
        mags_file = "{wdir}/{sample}/mags/MAGs.tsv",
        mags_general_file = "{wdir}/{sample}/MAGs.tsv",
    params:
        completness_threshold=config["ADDITIONAL_PARAM"]["completness_threshold"],
        contamination_threshold=config["ADDITIONAL_PARAM"]["contamination_threshold"],
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags"])) ) (config["USER_PARAMS"]["mags"]) 
    run:
        shell("mkdir -p {output.folder}/fasta")
        
        shell("touch {output.folder}/info.txt")
        shell('echo "Completeness {params.completness_threshold}" >> {output.folder}/info.txt')
        shell('echo "Contamination {params.contamination_threshold}" >> {output.folder}/info.txt')

        from geomosaic.parser.retrieve_survival_mags import retrieve_survival_mags

        checkm_table = os.path.join(str(input.checkm_folder), "checkm_output.tsv")
        das_tool_bins = os.path.join(str(input.dins_derep), "bins")
        mags_outfolder = str(output.folder)

        retrieve_survival_mags(checkm_table, das_tool_bins, params.completness_threshold, params.contamination_threshold, mags_outfolder, output.mags_general_file)
