---
title: Introduction
layout: about
nav_order: 2
---



# Introduction


Current metagenomics workflows can exploit three different streams of analysis: read-based, assembly-based, and binning-based. Read-based and/or assembly-based analyses are often neglected in favor of binning-driven inferences on the basis of their different reliability and sensitivity. However, the filtering steps involved in moving from reads to bins progressively reduce the potential amount of information, and thus the meaningfulness of the data obtained. There was, therefore, the need to create a metagenomic workflow that would combine these three different streams of analysis. Geomosaic was created to fit this purpose. It enables annotations to be performed on the three streams of analysis, and specially devised for the easy integration of the various programs and packages required. This approach maximizes the output of information gathered from raw data. 
Even so, Gemosaic flexibility allows the user to completely customize the analysis by choosing any stream of analysis, and to further tailor it with modules and packages. Thus, the Geomosaic workflow is sewed for the user purposes.


## Geomosaic Graph Structure

The base graph structure is made up of three main analyses that have to be taken into account when choosing the desired workflow:

| Stream | Module | Depends on |
|-------|------|--------|
| `Read-based`| Pre-processing | - |
| `Assembly-based`| Assembly | Pre-processing |
| `Binning-based`| Binning | Assembly, Pre-processing|

In fact, these dependencies can not be overlooked when generating the workflow with Geomosaic. For instance, ignoring the `Assembly` module hinders the execution of the `Binning` module exactly because of the dependency-based structure.

The full tree of dependencies among all modules is shown here.

![modules_DAG](assets/images/modules_DAG.png)

## Integrated modules

To summarise, the dependency tree has to be considered when ignoring specific modules, as they may inadvertently block other modules in the current or the next stream of analysis.

{: .important-title }
> 
> <table>
>     <thead>
>         <tr>
>             <th>Stream-level</th>
>             <th>Modules</th>
>             <th>Packages</th>
>         </tr>
>     </thead>
>     <tbody>
>         <tr>
>             <td rowspan=7>Read-based</td>
>             <td rowspan=3>Pre-processing</td>
>             <td>fastp</td>
>         </tr>
>         <tr>
>             <td>trimgalore</td>
>         </tr>
>         <tr>
>             <td>trimmomatic</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Reads QC</td>
>             <td>fastqc + reads count</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Functional Annotation</td>
>             <td>mi-faser</td>
>         </tr>
>         <tr>
>             <td rowspan=2>Taxonomic Annotation</td>
>             <td>Kaiju</td>
>         </tr>
>         <tr>
>             <td>MetaPhlAn</td>
>         </tr>
>         <tr>
>             <td rowspan=14>Assembly-based</td>
>             <td rowspan=2>Assembly</td>
>             <td>metaSPAdes</td>
>         </tr>
>         <tr>
>             <td>MEGAHIT</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Assembly Quality Check</td>
>             <td>quast</td>
>         </tr>
>         <tr>
>             <td rowspan=4>Read Mapping</td>
>             <td>Bowtie2</td>
>         </tr>
>         <tr>
>             <td>Bowtie2 - Output withou umapped reads</td>
>         </tr>
>         <tr>
>             <td>BBMap</td>
>         </tr>
>         <tr>
>             <td>BBMap - Output withou umapped reads</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Read Coverage</td>
>             <td>CoverM (Contigs)</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Taxonomic Annotation</td>
>             <td>Kraken 2</td>
>         </tr>
>         <tr>
>             <td rowspan=1>ORF Prediction</td>
>             <td>Prodigal</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Domain annotation</td>
>             <td>reCOGnizer</td>
>         </tr>
>         <tr>
>             <td rowspan=1>HMM Annotation</td>
>             <td>HMMsearch</td>
>         </tr>
>         <tr>
>             <td rowspan=2>Functional Annotation</td>
>             <td>eggNOG-mapper</td>
>         </tr>
>         <tr>
>             <td>KOfam Scan</td>
>         </tr>
>         <tr>
>             <td rowspan=11>Binning-based</td>
>             <td rowspan=1>Binning</td>
>             <td>Multi-Binners (Metabat2 + MaxBin2 + SemiBin2)</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Binning De-replication</td>
>             <td>DAS Tool</td>
>         </tr>
>         <tr>
>             <td rowspan=1>Binning Quality Assessment</td>
>             <td>CheckM</td>
>         </tr>
>         <tr>
>             <td rowspan=1>MAGs Retrieval</td>
>             <td>MAGs Retrieval</td>
>         </tr>
>         <tr>
>             <td rowspan=1>MAGs Metabolism Annotation</td>
>             <td>DRAM</td>
>         </tr>
>         <tr>
>             <td rowspan=1>MAGs Taxonomic Annotation</td>
>             <td>GTDB-Tk</td>
>         </tr>
>         <tr>
>             <td rowspan=1>MAGs ORF Prediction</td>
>             <td>Prodigal</td>
>         </tr>
>         <tr>
>             <td rowspan=1>MAGs Domain Annotation</td>
>             <td>reCOGnizer</td>
>         </tr>
>          <tr>
>             <td rowspan=1>MAGs Functional Annotation</td>
>             <td>KOfam Scans</td>
>         </tr>
>         <tr>
>             <td rowspan=1>MAGs Coverage</td>
>             <td>CoverM (Genome)</td>
>         </tr>
>         <tr>
>             <td rowspan=1>MAGs HMM annotation</td>
>             <td>HHMsearch</td>
>         </tr>
>     </tbody>
> </table>


### Modules that could be integrated in future
The following modules are under evaluation for future integration. 

__Read-based__:
- Functional annotation
    - mi-faser (with custom database)

__Assembly-based__:
- Functional Annotation:
    - Bakta
    - Prokka
- Taxonomic Annotation
    - cat/bat


However, if you know a module/package you would like to see integrated into Geomosaic, you can open an issue with all the information asking for this integration. At the moment, we accept only packages that can be installed from any Conda channel.
