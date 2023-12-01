
rule dram_db:
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["dram-setup"])) ) (config["USER_PARAMS"]["mags_dram"]) 
    output:
        dram_config_folder=directory(expand("{mags_dram_extdb_folder}", mags_dram_extdb_folder=config["EXT_DB"]["mags_dram"]))
    conda: config["ENVS"]["mags_dram"]
    shell:
        """
        mkdir -p {output.dram_config_folder}/dram_db

        DRAM-setup.py prepare_databases \
            --skip_uniref \
            --output_dir {output.dram_config_folder}/dram_db
        
        DRAM-setup.py export_config > {output.dram_config_folder}/dram_config.json
        """
