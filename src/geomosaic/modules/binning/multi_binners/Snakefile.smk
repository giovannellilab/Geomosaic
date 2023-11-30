
rule run_multi_binners:
    input:
        folder_readmap=expand("{wdir}/{sample}/{assembly_qc_readmapping}", assembly_qc_readmapping=config["assembly_qc_readmapping"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/multi_binners"),
        concoct_folder=directory("{wdir}/{sample}/multi_binners/concoct"),
        maxbin_folder=directory("{wdir}/{sample}/multi_binners/maxbin2"),
        metabat_folder=directory("{wdir}/{sample}/multi_binners/metabat2")
    threads: 5
    conda: config["ENVS"]["multi_binners"]
    params:
        concoct_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["multi_binners"]["concoct"])) ) (config["USER_PARAMS"]["multi_binners"]),
        maxbin_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["multi_binners"]["maxbin2"])) ) (config["USER_PARAMS"]["multi_binners"]),
        metabat_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["multi_binners"]["metabat2"])) ) (config["USER_PARAMS"]["multi_binners"])
    log: "{wdir}/{sample}/multi_binners/gm_log.out"
    shell:
        """
        mkdir -p {output.folder}

        echo "Executing Concoct..."
        cut_up_fasta.py {input.gm_contigs} {params.concoct_user_params} -o 0 -b {output.concoct_folder}/contigs_10K.bed > {output.concoct_folder}/contigs_10K.fa
        concoct_coverage_table.py {output.concoct_folder}/contigs_10K.bed {input.folder_readmap}/read_mapping_sorted.bam > {output.concoct_folder}/coverage_table.tsv
        concoct --composition_file {output.concoct_folder}/contigs_10K.fa --coverage_file {output.concoct_folder}/coverage_table.tsv -b {output.concoct_folder}/ >> {log} 2>&1
        merge_cutup_clustering.py {output.concoct_folder}/clustering_gt1000.csv > {output.concoct_folder}/clustering_merged.csv
        
        echo "Executing MetaBat2..."
        jgi_summarize_bam_contig_depths --outputDepth {output.metabat_folder}/metabat2_depth.txt {input.folder_readmap}/read_mapping_sorted.bam
        metabat2 {params.metabat_user_params} --inFile {input.gm_contigs} --abdFile {output.metabat_folder}/metabat2_depth.txt -o {output.metabat_folder}/output >> {log} 2>&1

        echo "Executing MaxBin2..."
        cut -f1,4,6,8,10 {output.metabat_folder}/metabat2_depth.txt > {output.maxbin_folder}/maxbin2_depth.txt
        run_MaxBin.pl {params.maxbin_user_params} -contig {input.gm_contigs} -abund {output.maxbin_folder}/maxbin2_depth.txt -thread {threads} -out {output.maxbin_folder}/output >> {log} 2>&1
        """


rule run_multi_binners_parser:
    input:
        concoct_folder="{wdir}/{sample}/multi_binners/concoct",
        maxbin_folder="{wdir}/{sample}/multi_binners/maxbin2",
        metabat_folder="{wdir}/{sample}/multi_binners/metabat2"
    output:
        concoct_bins=directory("{wdir}/{sample}/multi_binners/concoct/bins"),
        maxbin_bins=directory("{wdir}/{sample}/multi_binners/maxbin2/bins"),
        metabat_bins=directory("{wdir}/{sample}/multi_binners/metabat2/bins")
    run:
        from geomosaic.parsing_output.rename_bins import rename_bins
        
        shell("mkdir -p {output.concoct_bins}")
        shell("extract_fasta_bins.py {input.gm_contigs} {input.concoct_folder}/clustering_merged.csv --output_path {output.concoct_bins}")

        shell("mkdir -p {output.maxbin_bins}")
        shell("mv {input.metabat_folder}/*.fa {output.metabat_bins}/")

        shell("mkdir -p {output.metabat_bins}")
        shell("mv {input.maxbin_folder}/*.fasta {output.maxbin_bins}/")

        rename_bins(
            folder = os.path.join(str(input.concoct_folder), "bins"), 
            extension = "fa", 
            binner = "concoct"
        )

        rename_bins(
            folder = os.path.join(str(input.metabat_folder), "bins"), 
            extension = "fasta", 
            binner = "metabat2"
        )
    
        rename_bins(
            folder = os.path.join(str(input.maxbin_folder), "bins"), 
            extension = "fasta", 
            binner = "maxbin2"
        )
