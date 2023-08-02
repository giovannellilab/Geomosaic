
rule dram_setup_db:
    params:
        prepare_databases="prepare_databases"
    output:
        dram_config_folder=directory("{wdir}/dram_config"),
        db_folder=directory("/mnt/data/bigdata/dram_db")
    run:
        shell("mkdir -p {output.dram_config_folder}")
        shell("DRAM-setup.py {params.prepare_databases} \
            --skip_uniref \
            --output_dir {output.db_folder}")
        shell("DRAM-setup.py export_config > {output.dram_config_folder}/dram_config.json")

rule run_mags_dram:
    input:
        mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["mags_retrieval"], allow_missing=True),
        dram_config_folder="{wdir}/dram_config"
    output:
        directory("{wdir}/{sample}/mags_dram")
    threads: 15
    run:
        shell("DRAM.py annotate \
                --input_fasta '{input.mags_folder}/fasta/*.fa' \
                --checkm_quality {input.mags_folder}/MAGs.tsv \
                --output_dir {output} \
                --config_loc {input.dram_config_folder}/dram_config.json \
                --threads {threads}")
        shell("mkdir -p {output}/dram_distillation")
        shell("DRAM.py distill \
                -i {output}/annotations.tsv \
                -o {output}/dram_distillation \
                --trna_path {output}/trnas.tsv \
                --rrna_path {output}/rrnas.tsv")
