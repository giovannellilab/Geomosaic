
rule run_metaspades:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
    output:
        directory("{wdir}/{sample}/metaspades")
    threads: 5
    resources:
        mem_gb=45
    shell:
        """
        spades.py --meta --only-assembler -t {threads} -m {resources.mem_gb} -1 {input.r1} -2 {input.r2} -o {output}
        """
