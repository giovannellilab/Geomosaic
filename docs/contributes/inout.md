---
layout: default
title: "Modules dependencies: Input/Output"
parent: Contributes
nav_order: 11
---

<br>

# Modules Dependencies: Input and Output

<br>

In this section I'm describing the input and output that you should need to implement new packages for each module.

## pre_processing

### Input
For this module we need the original reads forward and reverse
```
r1="{wdir}/{sample}/R1.fastq.gz",
r2="{wdir}/{sample}/R2.fastq.gz",
```

### Output
In output we get processed reads, one forward and one reverse
```
r1="{wdir}/{sample}/fastp/R1.fastq.gz",
r2="{wdir}/{sample}/fastp/R2.fastq.gz"
```
