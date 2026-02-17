
rule rmi_rpi_indexes_custom_db:
    params:
        user_table = config["CUSTOM_DB"]["rmi_rpi_indexes"]["user_metal_table"],
        db="https://zenodo.org/records/10045253/files/KOs_sketched_scaled_1000.sig.zip",
        filename="KOs_sketched_scaled_1000.sig.zip"
    output:
        rmi_rpi_folder = directory(expand("{rmi_rpi_indexes_extdb_folder}", rmi_rpi_indexes_extdb_folder=config["EXT_DB"]["rmi_rpi_indexes"]["database_folder"])),
        table_file = expand("{table_file}", table_file = config["EXT_DB"]["rmi_rpi_indexes"]["table_file"])
    conda:
        config["ENVS_EXTDB"]["rmi_rpi_indexes"]
    message: "GEOMOSAIC MSG: Starting to setup the custom database for RM-RP Indexes"
    threads: 1
    shell:
        """
        mkdir -p {output.rmi_rpi_folder}/funprofiler_db

        cp {params.user_table} {output.table_file}
        

        curl --silent --output {output.rmi_rpi_folder}/funprofiler_db/{params.filename} {params.db}
        """
