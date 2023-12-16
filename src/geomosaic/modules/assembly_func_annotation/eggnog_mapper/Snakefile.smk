
rule run_eggnog_mapper:
    input:
        orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["orf_prediction"], allow_missing=True),
        db_folder=expand("{eggnog_mapper_extdb_folder}", eggnog_mapper_extdb_folder=config["EXT_DB"]["eggnog_mapper"])
    output:
        directory("{wdir}/{sample}/eggnog_mapper"),
    conda: config["ENVS"]["eggnog_mapper"]
    params:
        user_params_search = ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["eggnog_mapper_diamond_search"])) ) (config["USER_PARAMS"]["eggnog_mapper"]),
        user_params_annot = ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["eggnog_mapper_annotation"])) ) (config["USER_PARAMS"]["eggnog_mapper"]) 
    threads: config["threads"]
    shell:
        """
        mkdir -p {output}/tmp_search {output}/tmp_annot

        emapper.py \
            -m diamond \
            --sensmode more-sensitive \
            --no_annot \
            --cpu {threads} \
            --data_dir {input.db_folder}/ \
            -i {input.orf_predicted} \
            {params.user_params_search} \
            --temp_dir {output}/tmp_search \
            -o {output}/gm_eggnog

        emapper.py \
            -m no_search \
            --annotate_hits_table {output}/gm_eggnog.emapper.seed_orthologs \
            -o {output}/gm_eggnog_annot \
            --data_dir {input.db_folder}/ \
            --temp_dir {output}/tmp_annot \
            {params.user_params_annot} \
            --cpu {threads} \
            --excel \
            --dbmem
        
        (cd {output} && rm -r tmp_search {output}/tmp_annot)
        """
