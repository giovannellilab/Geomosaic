
rule run_das_tool:
    input:
        binning_path=expand("{wdir}/{sample}/{binning}", binning=config["binning"], allow_missing=True),
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/das_tool")
    threads: 5
    log: "{wdir}/{sample}/benchmark/das_tool.log"
    run:
        shell("mkdir -p {output.folder}")
        shell("Fasta_to_Contig2Bin.sh -i {input.binning_path}/concoct/bins -e fasta > {output.folder}/concoct_dastool.tsv")
        shell("Fasta_to_Contig2Bin.sh -i {input.binning_path}/maxbin2/bins -e fasta > {output.folder}/maxbin2_dastool.tsv")
        shell("Fasta_to_Contig2Bin.sh -i {input.binning_path}/metabat2/bins -e fasta > {output.folder}/metabat2_dastool.tsv")
        shell("""DAS_Tool -i {output.folder}/concoct_dastool.tsv,{output.folder}/maxbin2_dastool.tsv,{output.folder}/metabat2_dastool.tsv \
            -l concoct,maxbin2,metabat2 \
            -c {input.contig_path}/contigs.fasta \
            -o {output.folder}/das_tool \
            --write_bin_evals \
            --write_bins \
            --threads {threads} \
            --score_threshold 0.6 \
            --search_engine diamond
        """)
        shell("(cd {output.folder} && mv das_tool_DASTool_bins bins)")
