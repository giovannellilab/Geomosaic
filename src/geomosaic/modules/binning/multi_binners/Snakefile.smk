
rule run_multi_binners:
    input:
        sorted_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
        indexed_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam.bai", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True)
    output:
        maxbin_folder=directory("{wdir}/{sample}/multi_binners/maxbin2"),
        metabat_folder=directory("{wdir}/{sample}/multi_binners/metabat2"),
        semibin_folder=directory("{wdir}/{sample}/multi_binners/semibin2")
    threads: config["threads"]
    conda: config["ENVS"]["multi_binners"]
    params:
        maxbin_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["maxbin2"])) ) (config["USER_PARAMS"]["multi_binners"]),
        metabat_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["metabat2"])) ) (config["USER_PARAMS"]["multi_binners"]),
        semibin_user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["semibin2"])) ) (config["USER_PARAMS"]["multi_binners"])
    shell:
        """
        mkdir -p {output.maxbin_folder} {output.metabat_folder} {output.semibin_folder}
        
        echo "Executing MetaBat2..."
        jgi_summarize_bam_contig_depths --outputDepth {output.metabat_folder}/metabat2_depth.txt {input.sorted_bam}
        metabat2 {params.metabat_user_params} --inFile {input.gm_contigs} --abdFile {output.metabat_folder}/metabat2_depth.txt -o {output.metabat_folder}/output --numThreads {threads}

        echo "Executing MaxBin2..."
        cut -f1,4,6,8,10 {output.metabat_folder}/metabat2_depth.txt > {output.maxbin_folder}/maxbin2_depth.txt
        run_MaxBin.pl {params.maxbin_user_params} -contig {input.gm_contigs} -abund {output.maxbin_folder}/maxbin2_depth.txt -thread {threads} -out {output.maxbin_folder}/output

        echo "Executing SemiBin2..."
        SemiBin2 single_easy_bin {params.semibin_user_params} -i {input.gm_contigs} -o {output.semibin_folder} --depth-metabat2 {output.metabat_folder}/metabat2_depth.txt --threads {threads} --compression none
        """

rule run_multi_binners_parser:
    input:
        maxbin_folder = rules.run_multi_binners.output.maxbin_folder,
        metabat_folder = rules.run_multi_binners.output.metabat_folder,
        semibin_folder = rules.run_multi_binners.output.semibin_folder,
    output:
        maxbin_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_maxbin2_bins"),
        metabat_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_metabat2_bins"),
        semibin_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_semibin2_bins"),
        geomosaic_bins_trace=ensure("{wdir}/{sample}/multi_binners/geomosaic_bins.out", non_empty=True)
    params:
        multi_binners_folders="{wdir}/{sample}/multi_binners"
    run:
        from geomosaic.parser.rename_bins import rename_bins_to_fasta
        import glob
        import shutil
        import os

        shell("mkdir -p {output.metabat_bins}")
        shell("mkdir -p {output.maxbin_bins}")
        shell("mkdir -p {output.semibin_bins}")
        shell("touch {output.geomosaic_bins_trace}")

        metabat_count = 0
        for metabat_fasta_file in glob.glob(os.path.join(str(input.metabat_folder), "*.fa")):
            shutil.copy(metabat_fasta_file, str(output.metabat_bins))
            metabat_count += 1

        if metabat_count > 0:
            rename_bins_to_fasta(
                folder = str(output.metabat_bins), 
                extension = "fa", 
                binner = "metabat2"
            )
            shell("touch {params.multi_binners_folders}/metabat2_ok.out")
            shell("echo 'metabat2' >> {output.geomosaic_bins_trace}")

        maxbin_count = 0
        for maxbin_fasta_file in glob.glob(os.path.join(str(input.maxbin_folder), "*.fasta")):       
            shutil.copy(maxbin_fasta_file, str(output.maxbin_bins))
            maxbin_count += 1
        
        if maxbin_count > 0:
            rename_bins_to_fasta(
                folder = str(output.maxbin_bins), 
                extension = "fasta", 
                binner = "maxbin2"
            )
            shell("touch {params.multi_binners_folders}/maxbin2_ok.out")
            shell("echo 'maxbin2' >> {output.geomosaic_bins_trace}")
    
        semibin_count = 0
        for semibin_fasta_file in glob.glob(os.path.join(str(input.semibin_folder), "output_bins", "*.fa")):
            shutil.copy(semibin_fasta_file, str(output.semibin_bins))
            semibin_count += 1
        if semibin_count > 0:
            rename_bins_to_fasta(
                folder = str(output.semibin_bins), 
                extension = "fa", 
                binner = "semibin2"
            )
            shell("touch {params.multi_binners_folders}/semibin2_ok.out")
            shell("echo 'semibin2' >> {output.geomosaic_bins_trace}")
        
        # Check if file is empty and print error message due to the "ensure" snakemake condition
        if os.stat(str(output.geomosaic_bins_trace)).st_size == 0:
            print("GEOMOSAIC ERROR: All the Binners didn't provide any BINS.")
