---
layout: default
title: Installation
nav_order: 3
---


# Installation
This installation methodology is temporary. 

__*We are planning to provide Geomosaic as conda package. Stay tuned.*__

## Step 1
Clone the repository
```
git clone https://github.com/giovannellilab/Geomosaic.git

cd Geomosaic
```

All these steps must be performed inside the folder of the cloned github repository.

## Step 2
Install packages and modules

It is recommended to use mamba instead of conda (much faster!).
```
conda env create -f environment.yaml
```

or

(Recommended)

```
mamba env create -f environment.yaml
```

Now the geomosaic environment can be activated
```
conda activate geomosaic
```

## Step 3
Install the geomosaic package in the python environment

```
pip install .
```

