
rule run_checkm:
    input:
        dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["binning_derep"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True),
        db_folder=expand("{checkm_extdb_folder}", checkm_extdb_folder=config["EXT_DB"]["checkm"])
    output:
        folder=directory("{wdir}/{sample}/checkm")
    threads: config["threads"]
    conda: config["ENVS"]["checkm"]
    log: "{wdir}/{sample}/checkm/gm_log.out"
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["checkm"])) ) (config["USER_PARAMS"]["checkm"]),
        extension="--extension fa",
        tab_format="--tab_table",
    shell:
        """
        checkm data setRoot {input.db_folder}

        mkdir -p {output.folder}/plots
        
        echo "LINEAGE_WF"
        checkm lineage_wf \
            --threads {threads} \
            {params.tab_format} \
            {params.extension} \
            {params.user_params} \
            --quiet \
            --file {output.folder}/checkm_output.tsv \
            {input.dins_derep}/bins \
            {output.folder} >> {log} 2>&1
        
        echo "TETRA"
        checkm tetra -t {threads} --quiet {input.gm_contigs} {output.folder}/tetra.tsv >> {log} 2>&1
        echo "TETRA_PLOT"
        checkm tetra_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots {output.folder}/tetra.tsv 95 >> {log} 2>&1
        echo "DIST_PLOT"
        checkm dist_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots {output.folder}/tetra.tsv 95 >> {log} 2>&1
        echo "NX_PLOT"
        checkm nx_plot {params.extension} {input.dins_derep}/bins {output.folder}/plots >> {log} 2>&1
        echo "LEN_HIST"
        checkm len_hist {params.extension} {input.dins_derep}/bins {output.folder}/plots >> {log} 2>&1
        echo "MARKER_PLOT"
        checkm marker_plot {params.extension} {output.folder} {input.dins_derep}/bins {output.folder}/plots >> {log} 2>&1
        """
