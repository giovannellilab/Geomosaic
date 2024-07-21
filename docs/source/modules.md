
# Modules Dependencies

## Description
Geomosaic is a modular pipeline that allows for an easy customization of metagenomics workflows, through the choice of a single package for each module.

![geomosaic_modules](_static/images/modules_DAG.png)

At first look, each module may represents a type of analysis that can be performed during the metagenomics workflows. However, this description is useful but not complete as the following

```{admonition} Highlight
:class: important

A **module** is a type of metagenomics analysis that can be performed taking into consideration the dependencies to which it is linked. Therefore, a module will have specific dependencies if the package that implements that type of analysis will take in input the output of the linked modules.
```

Basically what matters most to define the dependencies among modules is the type of input and output of the corresponding packages. For instance, the module `assembly_readmapping` is very intuitive as the goal is to map the reads to the obtained assembly. Therefore, its dependencies are the `pre_processing` and the assembly, as we need the reads and the contigs file respectively. Indeed, in this read-mapping module, all the packages take in input the same objects and provide the same type of output (sam/bam file)

```{note}
As it is also important, that each package provides the same type of output, otherwise downstream modules may not work with all the possible choices of the user. 
```

So in this module, I can integrate all the packages that I want, as long as the input and the output are the same. In this case, the reads and the assembly as input, and as output two files are called `read_mapping_sorted.bam` and `read_mapping_sorted.bam.bai`.

Another simple example to understand this concept could be the **assembly**, which can be considered one of the main points in each metagenomics workflow, both for downstream analysis and technical requirements. At the time of writing, we have integrated two packages for this task: 
- _megahit_
- _metaspades_

Both require in input the processed reads. After their computation, they provide in output the same file, which in this case is called `geomosaic_contigs.fasta` (which is a subset of the original output file of each assembly, but filtered to remove contig with len < 1000). Since for both the input is the same, the corresponding module depends on the processing of the reads (`pre_processing`).

<br>

## What if two packages perform the same type of analysis but require different inputs?
This was the case of [integration example 3](contributes/magspackage.md), where we wanted to implement a package (KOfam Scan) for the functional annotation of the mags. Before that integration, the only package that belonged to this module was DRAM. However, DRAM usually takes in input a folder that contains all the fasta files of the mags, which is different from the input of the kofam scan, which takes the predicted orf from a metagenome (in this case MAG). Due to this difference, both packages cannot be in the same modules as the dependencies are different. 

Therefore for that integration, I decided to change the module belonging to DRAM, calling it `mags_metabolic_function` (and leaving it linked to the `mags_retrieval`) and inserting the `mags_kofam_scan` package in a new module called `mags_functional_annotation`, which depends on the `mags_orf_prediction`. 

Modules names are used in that way just to describe what the packages do, however, it would have been the same if it was `mags_functional_annotation` for DRAM and `mags_functional_annotation_2` for kofam scan.

