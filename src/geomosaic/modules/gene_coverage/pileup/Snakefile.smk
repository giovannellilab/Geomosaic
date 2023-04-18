
rule pileup:
    input:        
        prodigal_path=expand("{wdir}/{sample}/{orf_prediction}", orf_prediction=config["orf_prediction"], allow_missing=True),
        sam_path=expand("{wdir}/{sample}/{assembly_qc_readmapping}", assembly_qc_readmapping=config["assembly_qc_readmapping"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/pileup")
    params:
        hmm_folder=config["hmm_folder"]
    threads: 5
    run:
        shell("mkdir -p {output.folder}/hmm_search")
        for hmm in os.listdir(params.hmm_folder):
            if not hmm.endswith('.hmm'):
                continue
            
            filename=hmm.split(".hmm")[0]
            hmm_file=params.hmm_folder+"/"+hmm
            shell("hmmsearch --tblout /dev/stdout -o /dev/null --cpu {threads} --notextw {hmm_file} {input.prodigal_path}/protein_translations.faa | grep -v \"^#\" > {output.folder}/hmm_search/{filename}.hmm_results.txt")
        shell("cat {output.folder}/hmm_search/*.hmm_results.txt > {output.folder}/hmm_search/all_hmm_results.txt")
        shell("awk '{{print$1}}' {output.folder}/hmm_search/all_hmm_results.txt | sort -u >> {output.folder}/hmm_search/all_hits.txt")
        shell("pullseq -i {input.prodigal_path}/protein_translations.faa -n {output.folder}/hmm_search/all_hits.txt > {output.folder}/hmm_search/hmm_hits.fasta")
        shell("pileup.sh in={input.sam_path}/read_mapping.sam fastaorf={output.folder}/hmm_search/hmm_hits.fasta outorf={output.folder}/gene_coverage.tsv")
