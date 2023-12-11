
rule run_multi_binners:
    input:
        folder_readmap=expand("{wdir}/{sample}/{assembly_readmapping}", assembly_readmapping=config["assembly_readmapping"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/multi_binners"),
        concoct_folder=directory("{wdir}/{sample}/multi_binners/concoct"),
        maxbin_folder=directory("{wdir}/{sample}/multi_binners/maxbin2"),
        metabat_folder=directory("{wdir}/{sample}/multi_binners/metabat2")
    threads: config["threads"]
    conda: config["ENVS"]["multi_binners"]
    log: "{wdir}/{sample}/multi_binners/gm_log.out"
    params:
        concoct_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["concoct"])) ) (config["USER_PARAMS"]["multi_binners"]),
        maxbin_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["maxbin2"])) ) (config["USER_PARAMS"]["multi_binners"]),
        metabat_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["metabat2"])) ) (config["USER_PARAMS"]["multi_binners"])
    shell:
        """
        mkdir -p {output.concoct_folder}/bins {output.maxbin_folder} {output.metabat_folder}

        echo "Executing Concoct..."
        cut_up_fasta.py {input.gm_contigs} {params.concoct_user_params} -o 0 -b {output.concoct_folder}/contigs_10K.bed > {output.concoct_folder}/contigs_10K.fa
        echo "concoct_coverage_table.py"
        concoct_coverage_table.py {output.concoct_folder}/contigs_10K.bed {input.folder_readmap}/read_mapping_sorted.bam > {output.concoct_folder}/coverage_table.tsv
        echo "concoct"
        concoct --threads {threads} --composition_file {output.concoct_folder}/contigs_10K.fa --coverage_file {output.concoct_folder}/coverage_table.tsv -b {output.concoct_folder}/ >> {log} 2>&1
        echo "merge_cutup_clustering.py"
        merge_cutup_clustering.py {output.concoct_folder}/clustering_gt1000.csv > {output.concoct_folder}/clustering_merged.csv
        echo "extract_fasta_bins.py"
        extract_fasta_bins.py {input.gm_contigs} {output.concoct_folder}/clustering_merged.csv --output_path {output.concoct_folder}/bins
        
        echo "Executing MetaBat2..."
        jgi_summarize_bam_contig_depths --outputDepth {output.metabat_folder}/metabat2_depth.txt {input.folder_readmap}/read_mapping_sorted.bam
        metabat2 {params.metabat_user_params} --inFile {input.gm_contigs} --abdFile {output.metabat_folder}/metabat2_depth.txt -o {output.metabat_folder}/output --numThreads {threads} >> {log} 2>&1

        echo "Executing MaxBin2..."
        cut -f1,4,6,8,10 {output.metabat_folder}/metabat2_depth.txt > {output.maxbin_folder}/maxbin2_depth.txt
        run_MaxBin.pl {params.maxbin_user_params} -contig {input.gm_contigs} -abund {output.maxbin_folder}/maxbin2_depth.txt -thread {threads} -out {output.maxbin_folder}/output >> {log} 2>&1
        """

rule run_multi_binners_parser:
    input:
        concoct_folder = rules.run_multi_binners.output.concoct_folder,
        maxbin_folder = rules.run_multi_binners.output.maxbin_folder,
        metabat_folder = rules.run_multi_binners.output.metabat_folder,
    output:
        concoct_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_concoct_bins"),
        maxbin_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_maxbin2_bins"),
        metabat_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_metabat2_bins")
    run:
        from geomosaic.parser.rename_bins import rename_bins_to_fasta
        
        shell("mkdir -p {output.concoct_bins}")
        shell("cp {input.concoct_folder}/bins/*.fa {output.concoct_bins}/")

        shell("mkdir -p {output.metabat_bins}")
        shell("mv {input.metabat_folder}/*.fa {output.metabat_bins}/")

        shell("mkdir -p {output.maxbin_bins}")
        shell("mv {input.maxbin_folder}/*.fasta {output.maxbin_bins}/")

        rename_bins_to_fasta(
            folder = str(output.concoct_bins), 
            extension = "fa", 
            binner = "concoct"
        )

        rename_bins_to_fasta(
            folder = str(output.metabat_bins), 
            extension = "fasta", 
            binner = "metabat2"
        )
    
        rename_bins_to_fasta(
            folder = str(output.maxbin_bins), 
            extension = "fasta", 
            binner = "maxbin2"
        )
