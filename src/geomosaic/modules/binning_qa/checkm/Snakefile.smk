
rule run_checkm:
    input:
        bins_path=expand("{wdir}/{sample}/{binning}", binning=config["binning"], allow_missing=True),
        assembly_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True)
    output:
        directory("{wdir}/{sample}/checkm")
    threads: 5
    params:
        reduced_tree="--reduced_tree",
        extension="--extension fasta",
        tab_format="--tab_table",
        checkm_db="https://data.ace.uq.edu.au/public/CheckM_databases/checkm_data_2015_01_16.tar.gz"
    run:
        shell("mkdir -p {output}/plots {output}/database")
        shell("(cd {output}/database && wget {params.checkm_db} && tar -x -f *.tar.gz)")
        shell("checkm data setRoot {output}/database")
        shell("checkm lineage_wf --threads {threads} {params.tab_format} {params.reduced_tree} {params.extension} --file {output}/checkm_output.tsv {input.bins_path}/bins {output}")
        shell("checkm tetra -t {threads} --quiet {input.assembly_path}/contigs.fasta {output}/tetra.tsv")
        shell("checkm tetra_plot {params.extension} {output} {input.bins_path}/bins {output}/plots {output}/tetra.tsv 95")
        shell("checkm dist_plot {params.extension} {output} {input.bins_path}/bins {output}/plots {output}/tetra.tsv 95")
        shell("checkm nx_plot {params.extension} {input.bins_path}/bins {output}/plots")
        shell("checkm len_hist {params.extension} {input.bins_path}/bins {output}/plots")
        shell("checkm marker_plot {params.extension} {output} {input.bins_path}/bins {output}/plots")