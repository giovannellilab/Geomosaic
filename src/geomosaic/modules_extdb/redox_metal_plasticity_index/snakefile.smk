
rule redox_metal_plasticity_index_custom_db:
    params:
        user_table = config["CUSTOM_DB"]["redox_metal_plasticity_index"]["user_metal_table"],
        db="https://zenodo.org/records/10045253/files/KOs_sketched_scaled_1000.sig.zip",
        filename="KOs_sketched_scaled_1000.sig.zip"
    output:
        redox_metal_plasticity_index = directory(expand("{rmi_rpi_indexes_extdb_folder}", rmi_rpi_indexes_extdb_folder=config["EXT_DB"]["redox_metal_plasticity_index"]["database_folder"])),
        table_file = expand("{table_file}", table_file = config["EXT_DB"]["redox_metal_plasticity_index"]["table_file"])
    conda:
        config["ENVS_EXTDB"]["redox_metal_plasticity_index"]
    message: "GEOMOSAIC MSG: Starting to setup the custom database for RM-RP Indexes"
    threads: 1
    shell:
        """
        mkdir -p {output.redox_metal_plasticity_index}/funprofiler_db

        cp {params.user_table} {output.table_file}
        

        curl --silent --output {output.redox_metal_plasticity_index}/funprofiler_db/{params.filename} {params.db}
        """
