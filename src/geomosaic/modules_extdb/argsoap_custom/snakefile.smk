
rule argsoap_custom_db:
    params:
        user_fasta = config["CUSTOM_DB"]["argsoap_custom"]["user_protein_fasta"],
        user_mapping = config["CUSTOM_DB"]["argsoap_custom"]["user_mapping_file"]
    output:
        folder_db = directory(expand("{argsoap_custom_extdb_folder}", argsoap_custom_extdb_folder=config["EXT_DB"]["argsoap_custom"]["database_folder"])),
        argsoap_custom_fasta = expand("{argsoap_custom_fasta}", argsoap_custom_fasta = config["EXT_DB"]["argsoap_custom"]["protein_fasta"]),
        argsoap_custom_mapping = expand("{argsoap_custom_mapping}", argsoap_custom_mapping = config["EXT_DB"]["argsoap_custom"]["mapping_file"])
    conda: 
        config["ENVS_EXTDB"]["argsoap_custom"]
    message: "GEOMOSAIC MSG: Starting to setup the custom database for ARGs-OAP"
    threads: 1
    shell:
        """
        mkdir -p {output.folder_db}

        cp {params.user_fasta} {output.argsoap_custom_fasta}
        cp {params.user_mapping} {output.argsoap_custom_mapping}

        ( cd {output.folder_db} && args_oap make_db -i {output.argsoap_custom_fasta} ) 
        """
