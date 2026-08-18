# Introduction

Metagenomics enables the direct study of microbial communities from environmental samples, providing access to their taxonomic composition and functional potential without requiring cultivation. However, transforming metagenomic sequencing data into biological insight is computationally demanding and methodologically complex, particularly as datasets increase in size and analyses increasingly combine newly generated and publicly available data.

Geomosaic was developed to simplify this process while preserving analytical flexibility.

>Geomosaic does not treat read-based, assembly-based, and genome-resolved metagenomics as competing analytical strategies, but as complementary representations of the same biological system, each suited to answering different scientific questions.

## Why metagenomic analysis is challenging

Modern metagenomic studies often involve multiple sequential and parallel steps, including read preprocessing, taxonomic and functional profiling, assembly, gene prediction, genome reconstruction, annotation, read mapping, and abundance estimation.

The computational requirements of these analyses continue to increase because of:

- decreasing sequencing costs and larger numbers of samples;
- individual assemblies and co-assemblies;
- binning and co-binning;
- cross-sample read mapping;
- integration of newly generated and publicly available metagenomes;
- increasingly large comparative datasets.

These analyses often require High-Performance Computing (HPC) resources and familiarity with multiple bioinformatics tools, software dependencies, workflow managers, and computational environments.

Geomosaic addresses this complexity by integrating these steps within a modular, scalable, and reproducible workflow.

## Three complementary representations of metagenomic data

Metagenomic data can be analysed at three main levels: **reads, assemblies, and reconstructed genomes (MAGs)**. These analytical representations retain different fractions and dimensions of the original metagenomic information.

### Read-based analysis

Read-based analyses operate directly on quality-filtered sequencing reads.

They preserve the broadest representation of the sequenced community and are particularly useful for:

- community-wide taxonomic profiling;
- functional profiling;
- semi-quantitative comparisons of gene or taxon abundance across samples;
- detection of genes or organisms that may be poorly represented after assembly.

Their main limitation is the relatively limited sequence and genomic context provided by short sequencing fragments.

### Assembly-based analysis

Assembly-based approaches reconstruct sequencing reads into longer contigs.

This increases sequence completeness and enables:

- prediction of complete or near-complete genes;
- analysis of gene neighbourhoods;
- contig-level taxonomic and functional annotation;
- read mapping and coverage estimation;
- custom HMM-based analyses.

Assemblies, however, represent only the fraction of the community that can be successfully reconstructed. Low-abundance organisms, highly variable populations, repetitive regions, and highly complex communities may be underrepresented.

### Genome-resolved analysis

Genome-resolved metagenomics groups assembled contigs into metagenome-assembled genomes (MAGs).

MAGs provide the highest level of genomic context and enable:

- organism-level functional interpretation;
- genome-resolved metabolic reconstruction;
- taxonomic classification of reconstructed populations;
- analysis of gene content and genomic context;
- comparative genomics and pangenomics.

However, MAGs represent only the fraction of the community that can be successfully assembled, binned, and retained after genome-quality filtering.

For this reason, biological inferences derived from reads, assemblies, and MAGs should be interpreted according to the biological entity they represent: **the sequenced community, the assembled fraction of that community, and the recovered genomes, respectively.**

## The Geomosaic approach

Geomosaic integrates these three complementary analytical streams within a single environment:

Reads → Assemblies → MAGs

Rather than forcing users to select one analytical strategy, Geomosaic allows different representations of the same metagenomic dataset to be analysed together.

This makes it possible to move from broad community-level patterns to increasingly resolved genomic interpretation while retaining the information generated at each stage.

Geomosaic is built around a Directed Acyclic Graph (DAG) in which each node represents an analytical module and edges describe dependencies among modules. During workflow construction, the available choices dynamically change according to the modules selected by the user, ensuring that only valid analytical paths are generated.

The resulting workflow can therefore range from a single analytical module to a complete read-to-genome metagenomic analysis.

## Designed for different levels of expertise

Geomosaic was designed both for researchers approaching metagenomic analysis for the first time and for experienced bioinformaticians requiring greater control over workflow design.

For users getting started with metagenomics, Geomosaic provides:

- interactive workflow construction;
- automated generation of Snakemake workflows;
- automatic preparation of Conda environments;
- ready-to-run SLURM and GNU Parallel execution scripts;
- standardized project and sample organization;
- extensive documentation and walkthroughs.

More experienced users can:

- select alternative tools within individual modules;
- modify package parameters;
- start analyses from intermediate workflow stages;
- execute individual modules independently;
- provide custom databases and HMM collections;
- integrate additional packages or entirely new modules.

This combination of accessibility and extensibility is the basis of the mosaic-like architecture of Geomosaic.

## Geomosaic Graph Structure

Geomosaic is built around a Directed Acyclic Graph (DAG), in which each node represents an analytical module and edges define dependencies between modules. This structure ensures that only valid workflows are generated and allows the available module choices to change dynamically according to the user’s selections.

| Stream | Module | Depends on |
|-------|------|--------|
| `Read-based`| Pre-processing | - |
| `Assembly-based`| Assembly | Pre-processing |
| `Binning-based`| Binning | Pre-processing, Assembly |

For example, genome-resolved analyses depend on upstream assembly steps. If the `Assembly` module is skipped, downstream modules requiring assembled contigs are automatically removed from the available workflow.

The full tree of dependencies among all modules is shown here.

![modules_DAG](_static/images/modules_DAG.png)

## Scalable and analysis-ready

Geomosaic was designed for scalable execution on HPC systems and supports sample-level parallelization through SLURM and GNU Parallel.

In addition to executing bioinformatic workflows, Geomosaic includes a gather layer that integrates outputs generated across samples into standardized matrices and tables suitable for downstream statistical analysis and visualization.

These outputs can be further explored using the Geomosaic Cookbook, which provides reproducible R and Python workflows for data exploration, statistics, visualization, and figure generation.

## Explore Geomosaic

To continue:

See [Integrated modules](modules.md) for the current analytical modules and software packages.
See [Installation](installation.md) to install Geomosaic.
See the [Walkthrough](walkthrough.md) for a complete example analysis.
See [Commands](modules.md) for the command-line reference.
See [Contributing to Geomosaic](contributing.md) if you want to integrate new tools or modules.
