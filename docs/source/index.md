---
hide-toc: true
---

![Geomosaic](_static/images/geomosaic_logo_multicolor_300dpi.png)

<br> 

Welcome to the documentation of **Geomosaic**, a flexible and extensible bioinformatics platform integrating complementary metagenomic analyses from sequencing reads to genomes.

Geomosaic integrates **read-based, assembly-based, and genome-resolved analyses** within a single modular workflow. These complementary analytical streams provide different views of the same metagenomic dataset, from broad community-level profiling to increasingly resolved genomic and functional context.

Geomosaic is designed to lower the technical barrier to metagenomic analysis while retaining the flexibility required by experienced users. Automated workflow generation, ready-to-run execution scripts, modular analyses, and multiple entry points allow users to build and run complex metagenomic workflows without manually integrating individual software packages. More advanced users can modify parameters, execute individual modules, select alternative tools, or extend the platform with new modules and packages.

Geomosaic is designed for scalable execution on High-Performance Computing (HPC) systems using SLURM or GNU Parallel, while its modular architecture allows workflows to be tailored to different datasets and research questions.

If you want to know more about the philosophy behind Geomosaic, the different analytical streams, and what the platform can do for you, start with the [Introduction](introduction). If you want to get started immediately, jump directly to the [Installation](installation) instructions and then follow the [Tutorial](walkthrough/tutorial).

Already completed a Geomosaic analysis and ready to explore your results? Check out the [Geomosaic Cookbook](cookbook) and its companion GitHub repository for reproducible Jupyter notebooks and scripts for downstream analysis, visualization, and publication-ready figures.

Interested in extending Geomosaic? See the [Contributing to Geomosaic](contributes/index) section.


<!-- [Contributes](contributes/) -->

![gm](_static/images/gm.png)



```{toctree}
:caption: About Geomosaic
:hidden:

introduction
modules
Geomosaic cookbook
lastupdates
citation
```

```{toctree}
:caption: Getting started 
:hidden:

installation
update
```

```{toctree}
:caption: Commands
:hidden:

commands/index
commands/setup
commands/workflow
commands/unit
commands/prerun
commands/gather
```

```{toctree}
:caption: Walkthrough
:hidden:

walkthrough/summary
walkthrough/tutorial
```

```{toctree}
:caption: Tips
:hidden:

tips/suggestions
tips/faq
tips/specifictools
```

```{toctree}
:caption: Contributes
:hidden:

contributes/index
contributes/simplepackage
contributes/extdb
contributes/magspackage
contributes/io
```
