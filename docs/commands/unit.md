---
layout: default
title: geomosaic unit
parent: Commands
nav_order: 7
---

## `geomosaic unit`
It allows to choose and run just one module to execute an alternative package for that module. The command creates additional Snakefile and config file for the chosen modules in the geomosaic directory.

```
geomosaic unit --help
```

```
usage: geomosaic unit -s SETUP_FILE -m MODULE [-t THREADS] [-h]

DESCRIPTION: It allows to choose and run just one module, for example to execute an alternative package for that module. The command create another Snakefile a config file (both in the geomosaic directory) with the chosen module

Required Arguments:
  -s SETUP_FILE, --setup_file SETUP_FILE
                        Geomosaic setup file created from the geomosaic setup ... command.
  -m MODULE, --module MODULE
                        Modules to execute.

Optional Arguments:
  -t THREADS, --threads THREADS
                        Threads to use (per sample).

Available Modules:
  
  - pre_processing - Module: Pre processing with quality check
  - reads_qc - Module: Quality check (and/or Reads Count) of the reads after Pre-Processing
  - func_classification_rb - Module: Functional classification [Read-based]
  - tax_classification_rb - Module: Taxonomic classification [Read-based]
  - assembly - Module: Assembly
  - assembly_qc - Module: Assembly quality evaluation with metrics [Assembly-based]
  - assembly_readmapping - Module: Read mapping the processed reads to the Assembly [Assembly-based]
  - assembly_coverage - Module: Assembly coverage computation [Assembly-based]
  - assembly_tax_annotation - Module: Taxonomic Annotation on Assembly [Assembly-based]
  - orf_prediction - Module: perform ORF prediction [Assembly-based]
  - domain_annotation - Module: Domain annotation on Assembly [Assembly-based]
  - assembly_hmm_annotation - Module: tracking coverage for genes of interest through HMM models [Assembly-based]
  - assembly_func_annotation - Module: Functional Annotation on Assembly [Assembly-based]
  - binning - Module: Binning
  - binning_derep - Module: Binning Deeplication [Binning-based]
  - binning_qa - Module: Binning Quality Evaluation [Binning-based]
  - mags_retrieval - Module: get MAGs based on Contamination and Completeness threshold [Binning-based]
  - mags_metabolism_annotation - Module: Perform annotation of metabolism on filtered MAGs [Binning-based]
  - mags_tax_annotation - Module: Perform taxonomic annotation of filtered MAGs [Binning-based]
  - mags_orf_prediction - Module: perform ORF prediction for each retrieved MAG [Binning-based]
  - mags_domain_annotation - Module: perform domain-based annotation for each retrieved MAG [Binning-based]
  - mags_func_annotation - Module: perform functional annotation on ORF retrieved from filtered MAGs [Binning-based]
  - mags_coverage - Module: Computing read coverage for each retrieved MAG [Binning-based]
  - mags_hmm_annotation - Module: tracking coverage for genes of interest through HMM models on MAGs [Binning-based]

Help Arguments:
  -h, --help            show this help message and exit

```

## Arguments

This command has two required and two optional arguments:
- __REQUIRED__
    - (`-s`) Specifiy the name of the Geomosaic config file, obtained with the `setup` command.
    - (`-m`) Module where to start creating the workflow (Default: pre_processing)

- __OPTIONAL__
    - (`-t`) Threads to use (per sample)


### What to expect from this command
After completing this command, Geomosaic generates three files in its working directory:
- `Snakefile_unit.smk` - the Snakefile with the code for the chosen module and package.
- `config_unit.yaml` - the config file for snakemake execution.
- `Snakefile_extdb.smk` - Eventually, this file will be created by Geomosaic if the chosen module need an external data. Similarly to what described above for the `geomosaic workflow`, this file should be executed __before__ the `Snakefile_unit.smk`.

### Example usage `geomosaic unit`

**`IMPORTANT:` the following images may not refer to the modules that are integrated in the current version of Geomosaic. However, these images are very useful to understand how it works the creation of the single unit module.** 

```
geomosaic unit -s gmsetup_exp2023.yaml -m assembly -t 20
```

After executing this command, geomosaic will ask you for the desired package and then for the dependencies that have been run (which is not executed)

```
Geomosaic Process: Loading variables from Geomosaic setup file... 
--> OK <--

Module: Assembly
0) -- Ignore this module (and all successors) --
1) MetaSpades
2) MegaHit
1
Geomosaic Note: It is assumed also that those modules dependencies have already been run with Geomosaic
Geomosaic Note: 'assembly' depends on the following modules:
	- pre_processing

Now you need to specify the package/s that you used for those dependencies.

Module: Pre processing with quality check
0) -- Ignore this module (and all successors) --
1) fastp
2) Trim-Galore
3) Trimmomatic
1
Building DAG of jobs...
```

