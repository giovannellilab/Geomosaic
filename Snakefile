SAMPLES=['AG19_S52_L001_001',
'AG19_S52_L002_001',
'AG19_S52_L003_001',
'AG19_S52_L004_001',]

WDIR="raw_metagenomes/output_example"

rule targets:
  input:
    expand("{wdir}/{sample}/metaspades", sample=SAMPLES, wdir=WDIR)


rule run_metaspades:
    input:
        r1="{wdir}/{sample}/tg/R1_val_1.fq.gz",
        r2="{wdir}/{sample}/tg/R2_val_2.fq.gz",
    output:
        directory("{wdir}/{sample}/metaspades")
    threads: 5
    resources:
        mem_gb=25
    shell:
        """
        spades.py --meta --only-assembler -t {threads} -m {resources.mem_gb} -1 {input.r1} -2 {input.r2} -o {output}
        """
