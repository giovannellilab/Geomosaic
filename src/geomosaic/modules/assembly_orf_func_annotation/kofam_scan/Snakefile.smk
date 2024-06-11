
rule run_kofam_scan:
    input:
        orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True),
        db_folder=expand("{kofam_scan_extdb_folder}", kofam_scan_extdb_folder=config["EXT_DB"]["kofam_scan"])
    output:
        folder=directory("{wdir}/{sample}/kofam_scan"),
        tmp_dir=temp(directory("{wdir}/{sample}/kofam_scan/temp_geomosaic_dir"))
    conda: config["ENVS"]["kofam_scan"]
    params:
        user_params = ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["kofam_scan"])) ) (config["USER_PARAMS"]["kofam_scan"]),
        user_kofam_profiles = (lambda x: yaml.safe_load(open(x, "r"))["kofam_scan_profiles"]) (config["USER_PARAMS"]["kofam_scan"])
    threads: config["threads"]
    shell:
        """
        mkdir -p {output.folder}

        exec_annotation \
            {params.user_params} \
            --profile {input.db_folder}/{params.user_kofam_profiles} \
            --ko-list {input.db_folder}/ko_list \
            --cpu {threads} \
            --tmp-dir {output.tmp_dir} \
            -o {output.folder}/result.txt \
            {input.orf_predicted}
        """
