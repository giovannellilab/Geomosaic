
rule run_fastp:
    input:
        r1="{wdir}/{sample}/R1.fastq.gz",
        r2="{wdir}/{sample}/R2.fastq.gz",
    output:
        dir=directory("{wdir}/{sample}/fastp"),
        r1="{wdir}/{sample}/fastp/R1.fastq.gz", 
        r2="{wdir}/{sample}/fastp/R2.fastq.gz"
    threads: 5
    conda: config["ENVS"]["fastp"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["fastp"])) ) (config["USER_PARAMS"]["fastp"]) 
    shell:
        """
        fastp -i {input.r1} -I {input.r2} -o {output.r1} -O {output.r2} \
                --unpaired1 {output.dir}/unpaired_R1.fastq.gz \
                --unpaired2 {output.dir}/unpaired_R2.fastq.gz \
                --json {output.dir}/report.json \
                --html {output.dir}/report.html \
                --failed_out {output.dir}/failed.fastq.gz \
                --thread {threads} {params.user_params} -q 20 u 40
        """
