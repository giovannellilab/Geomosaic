# Frequently Asked Questions

<br>

Welcome to our section of _Frequently Asked Questions_. Over time, we plan to update this page based on the open issues. Since some questions and details are crucial for the correct execution of Geomosaic, you will likely see redundancy details as we already have explained in other parts of the documentation.

<br>

## How to ignore samples that failed a module computation
For instance, if the assembly failed for some samples, you can ignore them in the next modules when you are preparing the scripts with the `geomosaic prerun` (using the option `--ignore_samples`).


## How to submit an array job with the option to execute only a specific number of samples at the time?
Using Slurm specification, users can set a specific number of jobs in execution.
Once `geomosaic prerun` has been executed, you can modify the slurm script of geomosaic by adding `%2` to the line of the array job.
Specifically, the result should be something like this:
```
...
#SBATCH --array=1-32%2
...
```
meaning that slurm can only execute 2 jobs at the time. 


## How can I see the SLURM queue of my jobs
Let's assume that my account is `dcorso`, I can see the queue using the following commands `squeue -u dcorso` (specific for my account) or `squeue`.

```
squeue -u dcorso
```

## How can I check SLURM status of my jobs?
Assuming that you know which is the job ID (for example 123456), in clusters that have SLURM you can use the following command 
```
sacct -j 123456
```

If you are working with a TMUX session, we suggest to add `less` in pipe to be able to normal scroll with the mouse (To check)
```
sacct -j 123456 | less
```

This command is useful to see the logs and then the samples that failed a computation. For instance, if the assembly failed for some samples, you can ignore them in the next modules when you are preparing the scripts with the `geomosaic prerun` (using the option `--ignore_samples`).

## How can I use the same conda environments and external databases for different execute of Geomosaic?
As we have suggested also in the [Walkthrough tutorial](../walkthrough/tutorial.md#geomosaic-setup---command), it is a good practice to specify the same folder for the `-c` and `-e` options in the geomosaic setup, respectively for the conda environment and external databases.


## How can I add other options to the tools of my workflow?
Assuming that you already run `geomosaic workflow` / `geomosaic unit`, first you should know where is located your folder related to "GM USER PARAMETERS". If you don't know this information, you can retrieve it by opening the file called `gmsetup.yaml` (if you have specified the `-s` option during the `geomosaic setup` command, the corresponding filename could be different, so you should remember this). By opening such file, you can see the path related to the key `GM_USER_PARAMETERS`. Now in the terminal, change directory to this path, and you should be able to see many files with tool name that you have chosen. For example, if you chose `metaspades` for the _assembly_ module, you should see `metaspades.yaml`. Basically this is a text configuration file in which you can specify additional options for the corresponding tool as a bullet point list. 
For instance, let's assume that you are interested in adding the memory option for metaspades of 500 Gb (according to [metaspades documentation](http://ablab.github.io/spades/running.html#advanced-options)), you can open that file with `nano` (for example) and add that option, something like this:

`nano metaspades.yaml`

```
metaspades:
- -k 33,55,77,127
- --memory 500

seqkit:
- --min-len 2000
``` 

Save and close the file. That's it. Indeed, when the workflow is going to be executed, those file are read in order to add all the options that they contain, to the tool run.

__ALTERNATIVE__ (For more expert users): Although we do not suggest this way, you can modify the `Snakefile.smk` that was created after the `geomosaic workflow`, and add that option in the corresponding line of the execution of your tool of interest.


