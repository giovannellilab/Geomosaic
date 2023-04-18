
rule run_metabat2:
    input:
        folder_readmap=expand("{wdir}/{sample}/{assembly_qc_readmapping}", assembly_qc_readmapping=config["assembly_qc_readmapping"], allow_missing=True),
        contig_path=expand("{wdir}/{sample}/{assembly}", assembly=config["assembly"], allow_missing=True)
    output:
        folder=directory("{wdir}/{sample}/metabat2")
    threads: 5
    run:
        shell("mkdir -p {output.folder}/bins")
        shell("metabat2 --inFile {input.contig_path}/contigs.fasta --abdFile {input.folder_readmap}/metabat2_depth.txt -o {output.folder}/output")
        shell("mv {output.folder}/*.fa {output.folder}/bins/")
        shell('for file in {output.folder}/bins/*.fa; do  mv -- "$file" "${{file%.fa}}.fasta"; done;')
