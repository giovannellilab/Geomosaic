
rule m1_trimmomatic:
  input: 
    r1="{wdir}/{sample}/R1.fastq.gz",
    r2="{wdir}/{sample}/R2.fastq.gz",
  output:
    r1_paired="{wdir}/{sample}/trimmomatic/r1_paired.fastq.gz",
    r2_paired="{wdir}/{sample}/trimmomatic/r2_paired.fastq.gz",
    r1_unpaired="{wdir}/{sample}/trimmomatic/r1_unpaired.fastq.gz",
    r2_unpaired="{wdir}/{sample}/trimmomatic/r2_unpaired.fastq.gz",
  params:
    type_end="PE",
    leading=3,
    trailing=3,
    slidingwindow="4:15",
    minlen=36
  shell:
    """
    trimmomatic {params.type_end} \
    {input.r1} {input.r2} \
    {output.r1_paired} {output.r1_unpaired} \
    {output.r2_paired} {output.r2_unpaired} \
    LEADING:{params.leading} \
    TRAILING:{params.trailing} \
    SLIDINGWINDOW:{params.slidingwindow} \
    MINLEN:{params.minlen}
    """
