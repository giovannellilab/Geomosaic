
rule run_checkm_db:
    params:
        db_link="https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz"    
    output:
        db_folder=directory("{wdir}/checkm_db"),
    conda: config["ENVS"]["checkm"]
    shell:
        """
        mkdir -p {output.db_folder}
        (cd {output.db_folder} && wget {params.db_link} && tar -x -f *.tar.gz)
        checkm data setRoot {output.db_folder}
        """
