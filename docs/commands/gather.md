---
layout: default
title: geomosaic gather
parent: Commands
nav_order: 9
---

## `geomosaic gather`

This is an optional command that allows to create table `[obs x samples]` based on the obtained results of the executed workflows. It is avalaible only for some specific packages

```
geomosaic gather --help
```

```
usage: geomosaic gather -s SETUP_FILE [-f GATHER_FOLDER] [-p PACKAGES] [-u] [-h]

DESCRIPTION: This command is useful to gather all the results obtained from your workflow and create tables and data that are ready to use for downstream analysis.

Required Arguments:
  -s SETUP_FILE, --setup_file SETUP_FILE
                        Geomosaic setup file created from the geomosaic setup ... command.

Optional Arguments:
  -f GATHER_FOLDER, --gather_folder GATHER_FOLDER
                        Path where geomosaic can create the directory for gathering. Without any input, as default the folder 'gm_gathering' is created in
                        the working directory of Geomosaic.
  -p PACKAGES, --packages PACKAGES
                        a comma separated list of packages. Check the available packages in the section below. If you want to execute gather for specific
                        packages you can use this option as: --packages mifaser,kaiju,mags_gtdbtk,mags_dram.
  -u, --unit            Execute geomosaic gather considering the UNIT config file.

Available packages for Gathering:
  
  - mifaser
  - kaiju
  - kraken2
  - eggnog_mapper
  - recognizer
  - hmms_search
  - mags_gtdbtk
  - mags_recognizer
  - mags_dram
  - mags_hmmsearch
  - coverm_genome

Help Arguments:
  -h, --help            show this help message and exit
```

## Arguments

This command has both required and optional arguments.

- __REQUIRED__
    - (`-s`) Specifiy the name of the Geomosaic config file, obtained with the `setup` command.
- __OPTIONAL__
    - (`-f`) The path where Geomosaic can create the gather folder called `gm_gathering`. Without any inputs, it will be created in the Geomosaic `wdir`.
    - (`-p`) With this option, the user can specify as a comma separated list (without spaces) the packages of interest to create the gathering tables. Without any inputs, Geomosaic will execute gather for all the available packages.
    - (`-u`) This option is necessary if you want to execute the `gather` command taking into consideration the packages chosen in the `config_unit.yaml` file.


### Example usage `geomosaic gather`

Executing the gathering for all the available packages
```
geomosaic gather -s gmsetup_exp2023.yaml
```

Executing the gathering only for some packages and specifying the folder where to create the gather directory

```
geomosaic gather -s gmsetup_exp2023.yaml -p kaiju,mifaser,coverm_genome -f /home/davide/geomosaic_test/
```
