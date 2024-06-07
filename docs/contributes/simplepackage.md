---
layout: default
title: "Integration example 1: Simple Package"
parent: Contributes
nav_order: 12
---

# Integration example 1: Simple package
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

This tutorial will guide you through an integration of an example packages, which means one that doesn't need an **external database** or it is **not referred to MAGs module**.

**Module/Package Goal:**
- Stream-level: Read-based
- Module: `reads_qc`
- Package: `fastqc_readscount`

## Step 1: Clone/fork the repository

Since the final strategy is to make a pull request to the main repository, we suggest to fork our repo and then clone it (in the SSH way)
```
git@github.com:<YOURNAME>/Geomosaic.git
```

Remember to replace `<YOURNAME>` with your GitHub user account.

Once you have cloned the repository, open the directory created with the clone and also create another branch specifying the name of the package that you are going to integrate

```
git checkout -b fastqc
```


## Step 2: Create the module folder (if does not exists)
In this case we are going to integrate a package that should belongs to a module related to the quality checks of the reads after the `pre_processing` step, so we create a module folder called `reads_qc`. 

{: .important }
This step is necessary only if the module folder does not exists.

{: .highlight }
> {: .warning }
> __Do not__ use any special characters or insert spaces in the name.
>
> Just rely on _underscore_ and all lower-case characters


`<IMAGE>`


## Step 3: Create the package folder

In this step we only need to create the package folder insider the module of interest. In this case, I decided to call this program `fastqc_readscount`

{: .highlight }
> {: .warning }
> __Do not__ use any special characters or insert spaces in the name.
>
> Just rely on _underscore_ and all lower-case characters


## Step 4: Create package's snakefiles

Now we need to create the files for the code of the actual packge.
Inside the package folder, create 3 files named:
- `Snakefile.smk`
- `Snakefile_target.smk`
- `param.yaml`

For now you can leave them empty.

{: .important }
The names for this file are standard and are the same for each package.


## Step 5: Link the module/package to the Geomosaic core

So in this section we need to link our new module and/or our new package to the already existing core of Geomosaic, which is represented by the file called `gmpackages.json`

### Step 5.1: `order` section

Since `reads_qc` is a module that we thought to be after the processing of the reads, we put it after `pre_processing` but before the `assembly`.

`<IMAGE>`

### Step 5.2: `graph` section

{: .important }
> Before going further in this section, you should understand what really means a dependency in Geomosaic in this [section]()

The package that we are going to integrate in this module, depends on the output reads obtained from the `pre_processing` modules, so we put in graph the following line:

```python
["pre_processing", "reads_qc"],
```
    
### Step 5.3: `modules` section

In the correspongin `modules` section, we need to add the name of the module, which then must contain the following two keys 
- `description` - which contains a brief description of the module
- `choices` - which is a dictionary containing all the packages belonging to that module. <br>
    In particolar, the **key** (the blu string in the image) is the String that will come out in the terminal as a choice, during the workflow decision, while the **value** (in orange) is the actual name of the package, the one that we used also to create the folder created in step 3. 
    
    {: .important }
    Package name on the **value** must match with the folder created in the step 3
    
    {: .important }
    Remember the last comma after the last parenthesis.

    `<IMAGE>`

    - If the package does require any additional input, you can integrate this input in the corresponding section of "additional_input". For this package we don't need to put any additional argument
    - "envs" - name of the packages created in the step3 and name of the env file which must have the same name of the packages.
    - "external_db" - if you package does require an external database here you can specify some parameters (still to optimize)
        - each package has a key which contains two other keys
            - "inpfolder" must not be changed . its value should be the name of the package
            - "outfolder" must be the name of the folder. Usually we put the name of the package followed by the "_extdb" suffix. However, different package name maybe relay on the same external database like for "recognizer" and "mags_recognizer"
        For this package we don't need to specify anything for external database

    - gathering, this section if useful if we have some sort of script that is able to merge together the results from all the samples. In this case we can leave it like this


s6 - create the conda env for this package. In the folder envs we create a file with the name of the package with the yaml extension. And inside we can put all the necessary dependencies. In this case we are going to specify only fastqc from the bioconda channel. The reads count will be computed through a bash commands and thus we don't need any conda package. The name of the conda environment is the name of the package with "geomosaic_" as prefix.

Now we can write our code inside the Snakefile

s7 - In this case the code is very easy. Since this package only uses the processed reads, we can use the template of the assembly. We copy paste the code inside the snakefile.smk of metaspades and we modify it. 
We rename the name of the rule as the name of the packages with the prefix "run_". Our input section is fine, as we need only the reads from the Pre_processing module.
In output section usually we put the folder output that must be the same of the package name. The threads section is fine like this as it will going to get the number of threads from the config file.
The conda section, we are going only to substitute to metaspades the name of our package. So in this case, fastqc_readscount
The params section, in each package we use to put a params varaible called 'user_params' which are the one that are taken from the params in the folder gm_user_params. For this row in the snakefile we only need to put our package name where metaspades is.

And then we are going to write our code in our shell section.

So for this package we want to integrate the use of fastqc to check the quality of the reads, and then perform a reads count on the processed reads.

In our file Snakefile_target.smk we only need to the following rows. The name of the rule must be the same name of the package with the "all_" prefix. And then we need to change the rows in the input section, and we need to specify the same folder output.

Then we need to specify the header in yaml file, which must have the same package name, as all the parameters here we'll be read from the user_params in params section of the Snakefile.smk.

Now we can try the integrated package.

Activate the conda geomosaic. Updated geomosaic by doing pip install .

and then commit the changes.

