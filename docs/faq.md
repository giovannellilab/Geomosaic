---
layout: default
title: FAQ
nav_order: 16
---


# Frequently Asked Questions
{: .no_toc }

<br>

Welcome to our section of _Frequently Asked Questions_. Over time, we plan to update this page based on the open issues. Since some questions and details are crucial for the correct execution of Geomosaic, you will likely see redundancy details as we already have explained in other parts of the documentation.

<br>


<details open markdown="block">
  <summary>
    Table of contents
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>


## How can I check SLURM status of my jobs?
Assuming that you know which is the job id (for example 123456), you can use the following command
```
sacct -j 123456
```

If you are working with a TMUX session, we suggest to add `less` in pipe to be able to normal scroll with the mouse (To check)
```
sacct -j 123456 | less
```

## How can I use the same conda environments and external databases for different execute of Geomosaic?
As we have suggested also in the [Walkthrough](walkthrough#geomosaic-setup---command) tutorial, it is a good practice to specify the same folder for the `-c` and `-e` options in the geomosaic setup, respectively for the conda environment and external databases.


## How can I add other options to the tools of my warkflow?
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


