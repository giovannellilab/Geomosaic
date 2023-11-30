
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

rule run_checkm:
    input:
        dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["binning_derep"], allow_missing=True),
        assembly_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True),
        db_folder="{wdir}/checkm_db"
    output:
        folder=directory("{wdir}/{sample}/checkm")
    threads: 5
    conda: config["ENVS"]["checkm"]
    params:
        extension="--extension fa",
        tab_format="--tab_table",
    shell:
        """
        mkdir -p {output.folder}/plots
        
        checkm lineage_wf \
            --threads {threads} \
            {params.tab_format} \
            {params.extension} \
            {params.user_params} \
            --file {output.folder}/checkm_output.tsv \
            {input.dins_derep}/bins \
            {output.folder}
        
        checkm tetra -t {threads} --quiet {input.assembly_path}/contigs.fasta {output.folder}/tetra.tsv
        checkm tetra_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots {output.folder}/tetra.tsv 95
        checkm dist_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots {output.folder}/tetra.tsv 95
        checkm nx_plot {params.extension} {input.dins_derep}/bins {output.folder}/plots
        checkm len_hist {params.extension} {input.dins_derep}/bins {output.folder}/plots
        checkm marker_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots
        """
