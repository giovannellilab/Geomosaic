# Main commands

Geomosaic provides five main commands that together cover project setup, workflow construction, modular execution, workflow preparation, and downstream result aggregation.

- **_setup_**
  - Creates the Geomosaic working directory and the corresponding sample folders based on the provided sample table. It also generates the main Geomosaic configuration file (default name: `gmsetup.yaml`).

- **_workflow_**
  - Interactively guides the user through the selection of analytical modules and the corresponding software packages. Based on these choices, Geomosaic automatically generates a Snakefile containing the selected workflow, a Snakemake configuration file, and a graphical representation of the resulting workflow. All files are created within the Geomosaic project directory.

- **_unit_**
  - Executes a single analytical module independently of the complete workflow. This command is particularly useful for testing alternative software packages, rerunning individual analytical steps, modifying parameters, or evaluating different implementations of the same module. A dedicated Snakefile and configuration file are generated for the selected module.

- **_prerun_**
  - Prepares a workflow or a single module for execution by installing the required Conda environments and, optionally, generating ready-to-run execution scripts for High-Performance Computing (HPC) systems using either SLURM or GNU Parallel.

- **_gather_**
  - Collects results generated across all samples and integrates them into standardized tables and matrices that are immediately suitable for downstream statistical analysis, visualization, and data exploration.

Together, these five commands allow Geomosaic to accommodate different levels of user expertise. New users can generate and execute complete metagenomic workflows with minimal manual configuration, whereas advanced users can customize analyses at the level of individual modules, software packages, and workflow components.

## Command-line help

The complete list of available commands can be displayed at any time with:

```bash
geomosaic --help
```

which returns:

```none
usage: geomosaic [-h] [-v] {setup,workflow,unit,prerun,gather} ...

Geomosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

commands:
  {setup,workflow,unit,prerun,gather}
    setup               It creates the geomosaic working directory and the relative samples folders based on the provided sample table
    workflow            It allows to choose the desired modules and the relative packages. Based on your choices, the command creates a Snakefile (in the
                        Geomosaic directory) with the selected modules, the Snakemake configuration file, and a graph showing the generated workflow
    unit                It allows the execution of a single module, for example to evaluate an alternative package. The command generates a dedicated
                        Snakefile and configuration file for the selected module
    prerun              It installs the required Conda environments for the selected workflow or unit and optionally creates execution scripts for
                        running Geomosaic on HPC systems using SLURM or GNU Parallel
    gather              It gathers all results produced by the workflow and creates standardized tables and matrices for downstream analyses
```

Each command is described in detail in the following sections.