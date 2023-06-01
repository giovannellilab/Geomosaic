
rule run_multi_binners:
    input:
        folder_readmap=expand("{wdir}/{sample}/{assembly_qc_readmapping}", assembly_qc_readmapping=config["assembly_qc_readmapping"], allow_missing=True),
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/multi_binners")
    threads: 5
    log: "{wdir}/{sample}/multi_binners/gm_log.out"
    run:
        from geomosaic.parsing_output.rename_bins import rename_bins
        shell("mkdir -p {output.folder}")

        print("Executing Concoct...")
        concoct_folder=os.path.join(output.folder, "concoct")
        shell("mkdir -p {concoct_folder}/bins")
        shell("cut_up_fasta.py {input.contig_path}/contigs.fasta -c 10000 -o 0 --merge_last -b {concoct_folder}/contigs_10K.bed > {concoct_folder}/contigs_10K.fa")
        shell("concoct_coverage_table.py {concoct_folder}/contigs_10K.bed {input.folder_readmap}/read_mapping_sorted.bam > {concoct_folder}/coverage_table.tsv")
        shell("concoct --composition_file {concoct_folder}/contigs_10K.fa --coverage_file {concoct_folder}/coverage_table.tsv -b {concoct_folder}/ >> {log} 2>&1")
        shell("merge_cutup_clustering.py {concoct_folder}/clustering_gt1000.csv > {concoct_folder}/clustering_merged.csv")
        shell("extract_fasta_bins.py {input.contig_path}/contigs.fasta {concoct_folder}/clustering_merged.csv --output_path {concoct_folder}/bins")
        rename_bins(
            folder = os.path.join(concoct_folder, "bins"), 
            extension = "fa", 
            binner = "concoct"
        )

        print("Executing MaxBin2...")
        maxbin_folder=os.path.join(output.folder, "maxbin2")
        shell("mkdir -p {maxbin_folder}/bins")
        shell("run_MaxBin.pl -contig {input.contig_path}/contigs.fasta -abund {input.folder_readmap}/maxbin2_abundance.txt -thread {threads} -out {maxbin_folder}/output >> {log} 2>&1")
        shell("mv {maxbin_folder}/*.fasta {maxbin_folder}/bins/")
        rename_bins(
            folder = os.path.join(maxbin_folder, "bins"), 
            extension = "fasta", 
            binner = "maxbin2"
        )

        print("Executing MetaBat2...")
        metabat_folder=os.path.join(output.folder, "metabat2")
        shell("mkdir -p {metabat_folder}/bins")  
        shell("metabat2 --inFile {input.contig_path}/contigs.fasta --abdFile {input.folder_readmap}/metabat2_depth.txt -o {metabat_folder}/output >> {log} 2>&1")
        shell("mv {metabat_folder}/*.fa {metabat_folder}/bins/")
        rename_bins(
            folder = os.path.join(metabat_folder, "bins"), 
            extension = "fasta", 
            binner = "metabat2"
        )
