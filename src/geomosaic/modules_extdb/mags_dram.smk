
rule dram_setup_db:
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["dram-setup"])) ) (config["USER_PARAMS"]["mags_dram"]) 
    output:
        dram_config_folder=directory("{wdir}/dram_config")
    conda: config["ENVS"]["mags_dram"]
    shell:
        """
        mkdir -p {output.dram_config_folder}/dram_db
        DRAM-setup.py prepare_databases \
            --skip_uniref \
            --output_dir {output.dram_config_folder}/dram_db
        
        DRAM-setup.py export_config > {output.dram_config_folder}/dram_config.json
        """
