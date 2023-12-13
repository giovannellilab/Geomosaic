
rule run_mags_dram:
    input:
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["mags_retrieval"], allow_missing=True),
        dram_config_folder=expand("{mags_dram_extdb_folder}", mags_dram_extdb_folder=config["EXT_DB"]["mags_dram"])
    output:
        directory("{wdir}/{sample}/mags_dram")
    conda: config["ENVS"]["mags_dram"]
    threads: config["threads"]
    shell:
        """
        echo "DRAM Annotate"
        DRAM.py annotate \
                --input_fasta '{input.mags_folder}/fasta/*.fa' \
                --checkm_quality {input.mags_folder}/MAGs.tsv \
                --output_dir {output} \
                --config_loc {input.dram_config_folder}/dram_config.json \
                --threads {threads}
        
        echo "DRAM Distill"
        DRAM.py distill \
                --input_file {output}/annotations.tsv \
                --output_dir {output}/dram_distillation \
                --config_loc {input.dram_config_folder}/dram_config.json
        """
        
        
