# Suggestions

<br>

In this page you will find some basic suggestions about the Geomosaic execution that may help you. Over time, we plan to update this page based on our experience and the open issues.

<br>


## Execute commands with geomosaic conda environment activated
The geomosaic conda environment must be activate __before__ each command, even when submitting jobs through SLURM or executing the workflow using GNU Parallel. 

## Execute geomosaic commands in the same folder that contain `gmsetup.yaml`
In the [Walkthrough Tutorial](../walkthrough/tutorial.md#geomosaic-preparation-for-different-datasets) you can see that each command was executed in the same folder where the `gmsetup.yaml` was. We proposed this organization to work inside the root folder of the geomosaic computation of your dataset.

## Multiple users belonging to one group in Linux. How to handle shared data.
Often HPC cluster admins creates users that may belong to certain group, in order to let them have write/read permissions in a specific folder that may belong to the user's of your group.
If you would like to use Geomosaic for multiple datasets, you can start reading about the folder organization that we have proposed on our [Walkthrough Tutorial](../walkthrough/tutorial.md#macro-organization-of-the-folders). Moreover, the optimal scenario would be the possibility to use the already installed conda environments or already download external databases. For this purpose, we suggest to change the permission of the corresponding folders where conda environments are installed and external databases were downloaded. 

As group, we used Geomosaic on our data with a scenario like this, where a master folder called `GiovannelliLab` was created, where we were able to use different accounts, each one with permission to write and reads on that folder. Thus, in order to use conda environments and external databases that we already set up, we changed the corresponding folders permission with 

```
cd GiovannelliLab/utils/

chmod -R g+rwx geomosaic_condaenvs

chmod -R g+rwx geomosaic_extdb

```

### Install all the conda environments and download all the external databases before executing any workflow
Specifically, to allows multiple users having access to these folders, we suggest to install all the conda environments and download all the databases __before__ executing any command. This may be useful to prevent multiple users writing on the same folder, each one installing a conda environment and then retrieve which account you need to change permission of the installed conda env.

Basically, we used one account to install all the conda environments of the packages to which we were interested and download all the corresponding external dabatases. Thus we have created a workflow with these tools, and with the same account we executed first the `prerun` command (to install the conda envs) and then we run the `Snakefile_extdb.smk` file (using SLURM, to download all the extdb).

After all these steps were completed, we used the commands above to change the directory permissions

```
chmod -R g+rwx geomosaic_condaenvs

chmod -R g+rwx geomosaic_extdb
```

Following these steps we were able to use Geomosaic with different account, each referring its computation the same `geomosaic_condaenvs` and `geomosaic_extdb` without any error.

### Installing conda envs and extdb with different accounts
It may happen that one user may install a conda env (or download an extdb) that didn't exists before. In this scenario, after the execution of the `prerun` command we suggest to perform the above command to change permission in the corresponding installed conda envs (or download extdb).


## __[For Expert Users]__ Execution types of the workflow
To execute the created workflow, you can use the `prerun` command to create scripts for SLURM or GNU Parallel. When available we always suggest to use `--exec_type slurm` with the prerun. 

However, since the workflow is a Snakefile, if you are familiar with [Snakemake](https://snakemake.github.io) you can also use it to run the workflow. You will need to specify the following flags

- `--use-conda`
- `--conda-prefix <path to the geomosaic conda envs folder>` 

You can always refer to our [geomsoaic templates](https://github.com/giovannellilab/Geomosaic/blob/master/src/geomosaic/_slurm_templates.py)

Moreover, Snakemake has its own tutorial to execute the workflow using [SLURM](https://snakemake.readthedocs.io/en/stable/executing/cli.html#profiles).

