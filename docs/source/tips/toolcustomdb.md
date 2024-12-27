# Tools with custom database

In this page you will find some suggestion on how to setup custom db for specific tools.

<br>

## ARGs-OAP with Custom DB

(Module: `func_classification_rb`)

For detailed documentation, please refer to the ARGs-OAP Repository: [https://github.com/xinehc/args_oap](https://github.com/xinehc/args_oap)

I will try to simplify based also on my experience using this tool. Moreover some checks will be performed on the provided files to avoid later issues with the code. 

You need two files:

- A fasta file of protein sequences, named for example `sequences.fasta` (Do not put space in the filename).
We suggest to make this file as simple as possible. The header of each sequence should contain just the ID without any space, tab, or other irregular characters such as forward slash.
Avoid duplicated headers and duplicated sequences.

```
>id1
DQEATRFKT...
>id2
GWTRCMDCQ...
```


- A file named `mapping.tsv`, which is tab-separated. 
This file should contain at least one column, describing all the IDs of the fasta sequences. 
However you can put more columns, each one representing Class, Subclass or categories of your interests.
Do not put space in the column name. We suggest putting "_" instead of spaces. Geomosaic will make some checks.

```
IDs    Class    Subclass    Metal_Resistances
id1    class1    subclass1    iron
id2    class2    subclass2    iron
```
