# Update

Here you will find a short guide on how to update an older version of Geomosaic to the newest one!


```{important}
Execute all the steps with the `geomosaic` conda environment __activated__.
```

Assuming that you've created the environment by following the guide in the [Installation](installation.md#step-2---install-conda-environment) section, you can activate it with the following command

```bash
conda activate geomosaic
```

## Step 1 - Fetch last commits
Change your current directory to the one that has been created through the [`git clone` (during the installation)](installation.md#step-1---clone-the-repository). If you don't remember where it is located (or if it has been deleted), don't worry you can clone it again


::::{tab-set}

:::{tab-item} _Change directory_
```bash
cd Geomosaic
```
:::

:::{tab-item} _Clone it again_
```bash
git clone https://github.com/giovannellilab/Geomosaic.git

cd Geomosaic
```
:::
::::

Now you should _fetch last commits_
```
git pull
```

## Step 2 - update Geomosaic libraries

Staying in the `Geomosaic` directory, in this last step you should update the corresponding python libraries by running the following command

```
pip install . 
```

If all the steps have been successfully executed, you should see something like this
```none
...
Successfully built geomosaic
Installing collected packages: geomosaic
  Attempting uninstall: geomosaic
    Found existing installation: geomosaic 1.1.2
    Uninstalling geomosaic-1.1.2:
      Successfully uninstalled geomosaic-1.1.2
Successfully installed geomosaic-1.1.3
```

That's it! 
