
rule run_bbmap:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/bbmap"),
        sam_file="{wdir}/{sample}/bbmap/read_mapping.sam",
        bam_file="{wdir}/{sample}/bbmap/read_mapping.bam",
        sorted_bam="{wdir}/{sample}/bbmap/read_mapping_sorted.bam",
        indexed_bam="{wdir}/{sample}/bbmap/read_mapping_sorted.bam.bai"
    threads: 5
    run:
        shell("mkdir -p {output.folder}/stats")
        shell("""bbmap.sh threads={threads} ref={input.contig_path}/contigs.fasta \
            in={input.r1} in2={input.r2} out={output.sam_file} covstats={output.folder}/covstats.tsv nodisk \
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
        """)
        shell("samtools view -S -b {output.sam_file} > {output.bam_file}")
        shell("samtools sort {output.bam_file} -o {output.sorted_bam}")
        shell("samtools index {output.sorted_bam} {output.indexed_bam}")
        shell("jgi_summarize_bam_contig_depths --outputDepth {output.folder}/metabat2_depth.txt {output.sorted_bam}")
        shell("awk '{{print $1\"\t\"$2}}' {output.folder}/covstats.tsv | grep -v '^#' > {output.folder}/maxbin2_abundance.txt")
