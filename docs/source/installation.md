# Installation
Geomosaic has been designed to be straightforward to install and execute on Linux workstations and High-Performance Computing (HPC) systems.

> **New to metagenomics?** Geomosaic automatically creates the workflow, Conda environments, and HPC execution scripts, so you can get started without manually connecting dozens of independent software packages.

The current installation method uses a Conda environment that automatically installs all required software dependencies. Once installed, Geomosaic can generate complete workflows and execution scripts without requiring manual installation of individual bioinformatics packages.

```{note}
A Conda package for Geomosaic is currently under development and will simplify the installation process in future releases.
```

## Step 1 - Clone the repository
Clone the Geomosaic repository and move into the project directory.

```
git clone https://github.com/giovannellilab/Geomosaic.git

cd Geomosaic
```

All subsequent installation steps should be performed from within the cloned repository.

## Step 2 - Install conda environment

We recommend using [mamba](https://mamba.readthedocs.io/en/latest/) instead of Conda because it resolves package dependencies considerably faster.

::::{tab-set}

:::{tab-item} mamba
```bash
mamba env create -f environment.yaml
```
:::

:::{tab-item} conda
```bash
conda env create -f environment.yaml
```
:::
::::

<br>

Now the geomosaic environment can be activated
```
conda activate geomosaic
```

## Step 3 - Install the geomosaic package in the python environment

```
pip install .
```

## Verify the installation

To verify that the installation completed successfully, run:

```
geomosaic --help
```

If the installation was successful, the Geomosaic command-line interface and the list of available commands will be displayed.

