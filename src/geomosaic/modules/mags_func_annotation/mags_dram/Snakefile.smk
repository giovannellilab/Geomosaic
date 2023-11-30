
rule dram_setup_db:
    params:
        prepare_databases="prepare_databases",
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["dram-setup"])) ) (config["USER_PARAMS"]["dram"]) 
    output:
        dram_config_folder=directory("{wdir}/dram_config")
    conda: config["ENVS"]["dram"]
    shell:
        """
        mkdir -p {output.dram_config_folder}/dram_db
        DRAM-setup.py {params.prepare_databases} \
            --skip_uniref \
            --output_dir {output.dram_config_folder}/dram_db
        
        DRAM-setup.py export_config > {output.dram_config_folder}/dram_config.json
        """
        

rule run_mags_dram:
    input:
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["mags_retrieval"], allow_missing=True),
        dram_config_folder="{wdir}/dram_config"
    output:
        directory("{wdir}/{sample}/mags_dram")
    conda: config["ENVS"]["dram"]
    threads: 15
    shell:
        """
        DRAM.py annotate \
                --input_fasta '{input.mags_folder}/fasta/*.fa' \
                --checkm_quality {input.mags_folder}/MAGs.tsv \
                --output_dir {output} \
                --config_loc {input.dram_config_folder}/dram_config.json \
                --threads {threads}
        
        DRAM.py distill \
                --input_file {output}/annotations.tsv \
                --output_dir {output}/dram_distillation \
                --config_loc {input.dram_config_folder}/dram_config.json \
                --trna_path {output}/trnas.tsv \
                --rrna_path {output}/rrnas.tsv
        """
        
        
