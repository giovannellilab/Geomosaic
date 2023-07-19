
rule run_checkm_db:
    params:
        db_link="https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz"    
    output:
        db_folder="{wdir}/checkm_db",
    run:
        shell("mkdir -p {output.db_folder}")
        shell("(cd {output.db_folder} && wget {params.db_link} && tar -x -f *.tar.gz)")
        shell("checkm data setRoot {output.db_folder}")

rule run_checkm:
    input:
        dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["binning_derep"], allow_missing=True),
        assembly_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True),
        db_folder="{wdir}/checkm_db"
    output:
        folder=directory("{wdir}/{sample}/checkm")
    threads: 5
    params:
        reduced_tree="--reduced_tree",
        extension="--extension fa",
        tab_format="--tab_table",
    run:
        shell("mkdir -p {output.folder}/plots")
        shell("checkm lineage_wf \
            --threads {threads} \
            {params.tab_format} \
            {params.reduced_tree} \
            {params.extension} \
            --file {output.folder}/checkm_output.tsv \
            {input.dins_derep}/bins \
            {output.folder}")
        shell("checkm tetra -t {threads} --quiet {input.assembly_path}/contigs.fasta {output.folder}/tetra.tsv")
        shell("checkm tetra_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots {output.folder}/tetra.tsv 95")
        shell("checkm dist_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots {output.folder}/tetra.tsv 95")
        shell("checkm nx_plot {params.extension} {input.dins_derep}/bins {output.folder}/plots")
        shell("checkm len_hist {params.extension} {input.dins_derep}/bins {output.folder}/plots")
        shell("checkm marker_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots")
