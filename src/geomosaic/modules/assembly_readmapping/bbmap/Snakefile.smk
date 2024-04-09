
rule run_bbmap:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/bbmap"),
        sam_file=temp("{wdir}/{sample}/bbmap/read_mapping.sam"),
        bam_file=temp("{wdir}/{sample}/bbmap/read_mapping.bam"),
        sorted_bam=temp("{wdir}/{sample}/bbmap/read_mapping_sorted.bam"),
        indexed_bam=temp("{wdir}/{sample}/bbmap/read_mapping_sorted.bam.bai")
    threads: config["threads"]
    conda: config["ENVS"]["bbmap"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["bbmap"])) ) (config["USER_PARAMS"]["bbmap"]) 
    shell:
        """mkdir -p {output.folder}/stats"
        
        bbmap.sh {params.user_params} threads={threads} ref={input.gm_contigs} \
            in={input.r1} in2={input.r2} out={output.sam_file} covstats={output.folder}/covstats.tsv \
            bhist={output.folder}/stats/base_composition_by_pos_hist.txt \
            qhist={output.folder}/stats/quality_by_pos_hist.txt \
            aqhist={output.folder}/stats/average_read_quality_hist.txt \
            lhist={output.folder}/stats/read_length_hist.txt \
            ihist={output.folder}/stats/inserted_size_hist.txt \
            ehist={output.folder}/stats/error_per_read_hist.txt \
            qahist={output.folder}/stats/quality_accuracy_hist.txt \
            indelhist={output.folder}/stats/indel_length_hist.txt \
            mhist={output.folder}/stats/match_sub_del_ins_rates_by_location.txt \
            gchist={output.folder}/stats/gc_content_hist.txt \
            idhist={output.folder}/stats/read_count_vs_perc_identity_hist.txt \
            scafstats={output.folder}/stats/reads_mapped_to_scaffold.txt
        
        samtools view -@ {threads} -S -b {output.sam_file} > {output.bam_file}

        samtools sort -@ {threads} {output.bam_file} -o {output.sorted_bam}

        samtools index -@ {threads} {output.sorted_bam} {output.indexed_bam}
        """
