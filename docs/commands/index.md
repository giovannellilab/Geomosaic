---
layout: default
title: Commands
nav_order: 4
has_children: true
has_toc: false
---


# Commands
{: .no_toc }

<br>

<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

-----

## Main cmds

Geomosaic pipeline has five main commands:
- _setup_
    - It creates the Geomosaic working directory and the relative sample folders based on the provided sample table, together with a Geomosaic config file (whose default name is: `gmsetup.yaml`)
- _workflow_
    - It allows the user to choose the modules and the relative packages to be used. Based on these choices, the command generates a Snakefile with the selected modules, a config file for snakemake, and a graph image to show the created workflow; the mentioned files are created in the Geomosaic directory.
- _unit_
    - It enables the selection of a module the user wants to execute with an alternative package. The command generates another Snakefile and a config file with the chosen module, both in the Geomosaic directory.
- _prerun_
    - This command allows you to install the required conda environments of your workflow/unit and (OPTIONAL) to create required scripts to execute Geomosaic on a cluster using SLURM
- _gather_
    - This command is useful to gather all the results obtained from your workflow and create tables and data that are ready to use for downstream analysis.

```
geomosaic --help
```

```
usage: geomosaic [-h] [-v] {setup,workflow,unit,prerun,gather} ...

Geomosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

commands:
  {setup,workflow,unit,prerun,gather}
    setup               It creates the geomosaic working directory and the relative samples folders based on the provided sample table
    workflow            It allows to choose the desired modules and the relative packages. Based on you choices, the command will create a Snakefile (in the
                        geomosaic directory) with the chosen modules, the config file for snakemake, and a graph image to show the created workflow
    unit                It allows to choose and run just one module, for example to execute an alternative package for that module. The command create
                        another Snakefile a config file (both in the geomosaic directory) with the chosen module
    prerun              This command is usefull to install the required conda environments of your workflow/unit and create required scripts to execute
                        Geomosaic on a cluster using SLURM
    gather              This command is useful to gather all the results obtained from your workflow and create tables and data that are ready to use for
                        downstream analysis.
```

## Walkthrough Image

We also suggest to have a look to our [Walkthrough tutorial](../walkthrough) for a more complete overview of Geomosaic procedure!

<img src="assets/images/geomosaic_commands.svg">
