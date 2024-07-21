---
tocdepth: 3
---

# Input and Output of each modules

This section reports the input and output that you should need to implement new packages for each module.

## Read-Based
### pre_processing

#### Input
```python
r1="{wdir}/{sample}/R1.fastq.gz",
r2="{wdir}/{sample}/R2.fastq.gz",
```

#### Output
```python
r1="{wdir}/{sample}/fastp/R1.fastq.gz",
r2="{wdir}/{sample}/fastp/R2.fastq.gz"
```

<br>

### reads_qc

#### Input
```python
r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### func_classification_rb

#### Input
```python
r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### tax_classification_rb

#### Input
```python
r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

## Assembly-based
### assembly

#### Input
```python
r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
```

#### Output
```python
output_fasta="{wdir}/{sample}/metaspades/geomosaic_contigs.fasta",
```

<br>

### assembly_readmapping

#### Input
```python
r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True)
```

#### Output
```python
sorted_bam="{wdir}/{sample}/bowtie2/read_mapping_sorted.bam",
indexed_bam="{wdir}/{sample}/bowtie2/read_mapping_sorted.bam.bai"
```

<br>

### assembly_qc

#### Input
```python
gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### assembly_coverage

#### Input
```python
sorted_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
indexed_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam.bai", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### assembly_tax_annotation

#### Input
```python
gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### orf_prediction

#### Input
```python
gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True),
```

#### Output
```python
output_fasta = "{wdir}/{sample}/prodigal/orf_predicted.faa",
output_simple_mapping = "{wdir}/{sample}/prodigal/simple_orf_contig_mapping.tsv", 
```

<br>

### assembly_func_annotation

#### Input
```python
orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### domain_annotation

#### Input
```python
orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### assembly_hmm_annotation

#### Input
```python
orf_predicted = expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True),
orf_simple_mapping = expand("{wdir}/{sample}/{orf_prediction}/simple_orf_contig_mapping.tsv", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True), 
coverage_folder = expand("{wdir}/{sample}/{assembly_coverage}", assembly_coverage=config["MODULES"]["assembly_coverage"], allow_missing=True)
```

#### Output
No specific output for downstream modules.

<br>

## Binning-based
### binning

#### Input
```python
sorted_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
indexed_bam=expand("{wdir}/{sample}/{assembly_readmapping}/read_mapping_sorted.bam.bai", assembly_readmapping=config["MODULES"]["assembly_readmapping"], allow_missing=True),
gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True)
```

#### Output
```python
maxbin_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_maxbin2_bins"),
metabat_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_metabat2_bins"),
semibin_bins=directory("{wdir}/{sample}/multi_binners/geomosaic_semibin2_bins")
```

<br>

### binning_derep

#### Input
```python
semibin_bins=expand("{wdir}/{sample}/{binning}/geomosaic_semibin2_bins", binning=config["MODULES"]["binning"], allow_missing=True),
maxbin_bins=expand("{wdir}/{sample}/{binning}/geomosaic_maxbin2_bins", binning=config["MODULES"]["binning"], allow_missing=True),
metabat_bins=expand("{wdir}/{sample}/{binning}/geomosaic_metabat2_bins", binning=config["MODULES"]["binning"], allow_missing=True),
gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True)
```

#### Output
No specific output for downstream modules.

<br>

### binning_qa

#### Input
```python
dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["MODULES"]["binning_derep"], allow_missing=True),
gm_contigs=expand("{wdir}/{sample}/{assembly}/geomosaic_contigs.fasta", assembly=config["MODULES"]["assembly"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### mags_retrieval

#### Input
```python
dins_derep=expand("{wdir}/{sample}/{binning_derep}", binning_derep=config["MODULES"]["binning_derep"], allow_missing=True),
checkm_folder=expand("{wdir}/{sample}/{binning_qa}", binning_qa=config["MODULES"]["binning_qa"], allow_missing=True)
```

#### Output
```python
folder = directory("{wdir}/{sample}/mags"),
mags_file = "{wdir}/{sample}/mags/MAGs.tsv",
mags_general_file = "{wdir}/{sample}/MAGs.tsv",
```

<br>

### mags_metabolism_annotation

#### Input
```python
mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### mags_tax_annotation

#### Input
```python
mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### mags_orf_prediction

#### Input
```python
fasta=expand("{wdir}/{sample}/{mags_retrieval}/fasta/{mag}.fa", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True)
```

#### Output
```python
output_fasta = "{wdir}/{sample}/mags_prodigal/{mag}/orf_predicted.faa",
output_simple_mapping = "{wdir}/{sample}/mags_prodigal/{mag}/simple_orf_contig_mapping.tsv",
```

<br>

### mags_domain_annotation

#### Input
```python
mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/orf_predicted.faa", mags_orf_prediction=config["MODULES"]["mags_orf_prediction"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### mags_func_annotation

#### Input
```python
mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/orf_predicted.faa", mags_orf_prediction=config["MODULES"]["mags_orf_prediction"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### mags_coverage

#### Input
```python
r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
mags_folder=expand("{wdir}/{sample}/{mags_retrieval}", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True),
```

#### Output
No specific output for downstream modules.

<br>

### mags_hmm_annotation

#### Input
```python
mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/orf_predicted.faa", mags_orf_prediction=config["MODULES"]["mags_orf_prediction"], allow_missing=True),
```

#### Output
No specific output for downstream modules.
