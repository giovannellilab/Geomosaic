
rule run_mags_prodigal:
    input:
        fasta=expand("{wdir}/{sample}/{mags_retrieval}/fasta/{mag}.fa", mags_retrieval=config["mags_retrieval"], allow_missing=True)
    output:
        genes_gff="{wdir}/{sample}/mags_prodigal/{mag}/genes.gff",
        protein_translations="{wdir}/{sample}/mags_prodigal/{mag}/protein_translations.faa",
    params:
        meta="-p meta",
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags_prodigal"])) ) (config["USER_PARAMS"]["mags_prodigal"]) 
    conda: config["ENVS"]["mags_prodigal"]
    threads: 1
    shell:
        """
        prodigal -i {input.fasta} \
            -o {output.genes_gff} \
            -a {output.protein_translations} \
            -f gff \
            {params.meta} \
            {params.user_params}
        """

rule run_parse_mags_prodigal:
    input:
        fasta_input=rules.run_mags_prodigal.output.protein_translations # I love this snakemake feature, use it as much as possible
    output:
        output_mapping = "{wdir}/{sample}/mags_prodigal/{mag}/orf_contig_mapping.tsv",
        output_fasta = "{wdir}/{sample}/mags_prodigal/{mag}/orf_predicted.faa",
        output_simple_mapping = "{wdir}/{sample}/mags_prodigal/{mag}/simple_orf_contig_mapping.tsv",
    threads: 1
    run:
        from geomosaic.parser.prodigal_orf_mapping import parsing_prodigal_orfs    
        parsing_prodigal_orfs(str(input.fasta_input), str(output.output_mapping), str(output.output_fasta), str(output.output_simple_mapping))

def ls_collect_bins(f_string): 
    def _f(wildcards):
        import pandas as pd

        mags_file = checkpoints.run_mags.get(**wildcards).output.mags_file
        df_mags = pd.read_csv(mags_file, sep="\t")
        
        _temp = []
        for m in df_mags.MAGs:
            _temp.append(f_string.format(mag=m, **wildcards) )

        return _temp
    return _f

checkpoint gather_mags_prodigal_outputs:
    input: 
        collected=ls_collect_bins("{wdir}/{sample}/mags_prodigal/{mag}/orf_predicted.faa"),
        mags_tsv=expand("{wdir}/{sample}/{mags_retrieval}/MAGs.tsv", mags_retrieval=config["mags_retrieval"], allow_missing=True)
    output: 
        gather=touch("{wdir}/{sample}/mags_prodigal/gather_OK.txt"),
        mags_file="{wdir}/{sample}/mags_prodigal/MAGs.tsv"
    threads: 1
    run:
        shell("cp {input.mags_tsv} {output.mags_file}")
