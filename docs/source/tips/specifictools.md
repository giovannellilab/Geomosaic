# Tips on specific tools

In this page you will find suggestions on how to optimize the execution of some tools, based on our experience.
Have a look on the table of content in the right side of the page. 

<br>

## ARGs-OAP with Custom DB

(Module: `func_classification_rb`)

For detailed documentation, please refer to the ARGs-OAP Repository: [https://github.com/xinehc/args_oap](https://github.com/xinehc/args_oap)

I will try to simplify based also on my experience using this tool. Moreover some checks will be performed on the provided files to avoid later issues with the code. 

To use this tool, you will need two files:

1) A fasta file of protein sequences, named for example `sequences.fasta` (Do not put space in the filename).
We suggest to make this file as simple as possible. The header of each sequence should contain just the ID without any space, tab, or other irregular characters such as forward slash.
Avoid duplicated headers and duplicated sequences.

```
>id1
DQEATRFKT...
>id2
GWTRCMDCQ...
```


2) A file (for example named `mapping.tsv`) for mapping the IDs in the sequences file to categories of interest, and it must be tab-separated. This file should contain at least one column, describing all the IDs of the fasta sequences. 
However you can put more columns, each one representing Class, Subclass or categories of your interests.
Do not put space in the column name. We suggest putting "_" instead of spaces. Geomosaic will make some checks.

```
IDs    Class    Subclass    Metal_Resistances
id1    class1    subclass1    iron
id2    class2    subclass2    iron
```

Moreover, Geomosaic will start asking some questions.

__The first question is the following:__

```none
[ADDITIONAL PARAMETER REQUEST - CUSTOM DB for ARGs-OAP - FASTA FILE]
Description: you need to specify the path to the protein fasta file for the custom DB of ARGs-OAP

```

Geomosaic is asking for the `absolute path` to the file described above in point `1)`:
`/path/to/folder/sequences.fasta`

<br>

__The second question will regard the file described above in point `2)`:__
```none
[ADDITIONAL PARAMETER REQUEST - CUSTOM DB for ARGs-OAP - Mapping FILE]
Description: you need to specify the path to the mapping file for the custom DB of ARGs-OAP

```
`/path/to/folder/mapping.tsv`

<br>

__The third question will regard a custom name that you can provide for your database__  

```none
[ADDITIONAL PARAMETER REQUEST - CUSTOM DB for ARGs-OAP - Database folder]
Description: you need to specify a name for the custom database folder. For example, if this argsoap custom will concern hydrogenases, you may want to rename the database folder as 'argsoap_custom_hydrogenases'"
```

`argsoap_custom_hydrogenases`


```{admonition} Suggestion
:class: important

If you already have created a database using this tool/module, you can type the same name to refer and use it. 
```

Indeed, by doing this you can avoid executing the script for creating the external db (`slurm_extdb_geomosaic.sh` or `parallel_extdb_geomosaic.sh`).

<br>


__The fourth question will regard a custom name for the output folder__

```
[ADDITIONAL PARAMETER REQUEST - CUSTOM DB for ARGs-OAP - Output folder]
Description: you need to specify a name for the output folder. For example, if this argsoap custom will concern hydrogenases, you may want to rename the output folder as 'argsoap_custom_hydrogenases'
```

Since this tool can be used with a custom db, Geomosaic is asking this question to let you choose a custom name for the output folder. The idea is to have a specific name for a specific database of interest and execution. This will allow to run the tool with different databases and have several output folders, each one with its own name.

`argsoap_custom_hydrogenases`

Indeed, you will find a folder called with your prompted name inside of each sample.


## Metaspades

(Module: `assembly`)

For detailed documentation, please refer to the Spades Repository: [http://ablab.github.io/spades/](http://ablab.github.io/spades/)

I will try to simplify based also on my experience using this tool. 

Assembly is a main bottleneck of metagenomics execution as it may require a lot of memory (RAM). However, for metaspades as you can see here [http://ablab.github.io/spades/running.html#advanced-options](http://ablab.github.io/spades/running.html#advanced-options), the default memory setting is 250 Gb. This may prevent the right execution of the assembly even if you set a higher value of the `--memory` during the `geomosaic prerun`, as the latter will only affects slurm resources.

__For this reason, we always suggest overwriting the default value of 250 Gb, by adding the `--memory` option in the corresponding yaml file in the GM_USER_PARAMETERS folder, and then also set the memory in the `geomosaic prerun` very similar to this value, maybe an higher value could be better just to be sure.__


```{admonition} Suggestion
:class: important

If you don't know where the "GM USER PARAMETERS" folder is located, you can retrieve it by opening the file called `gmsetup.yaml`
```

Inside this folder you should see `metaspades.yaml`. 


```{admonition} Suggestion
:class: important

Basically this is a text configuration file in which you can specify additional options for the corresponding tool as a bullet point list. 
```

> `nano metaspades.yaml`

```
metaspades:
- -k 33,55,77,127
- --memory 500

seqkit:
- --min-len 2000
``` 

and then, during the `geomosaic prerun` you can have

`geomosaic prerun ... -m 505`


## Megahit

(Module: `assembly`)

For detailed documentation, please refer to the Spades Repository: [https://github.com/voutcn/megahit/wiki](https://github.com/voutcn/megahit/wiki)

I will try to simplify based also on my experience using this tool. 

Memory documentation of Megahit [https://github.com/voutcn/megahit/wiki/MEGAHIT-Memory-setting](https://github.com/voutcn/megahit/wiki/MEGAHIT-Memory-setting)

Similarly to what was described in the [metaspades section](#metaspades), in this case you can specify memory value in `BYTES` by adding the corresponding option to the `megahit.yaml` file in the `GM_USER_PARAMETERS` folder.


> `nano megahit.yaml`

```
megahit:
# More Sensitive, but slower
- --presets meta-sensitive
- --memory 500000000000

seqkit:
- --min-len 2000
``` 

and then, during the `geomosaic prerun` you can have

`geomosaic prerun ... -m 505`


