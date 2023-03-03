# GeoMosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis

Create the conda environment:
```
conda env create -f environment.yaml
```


## Modules

This pipeline is organized in modules:
<ul>
  <li>Module 1: reads quality check</li>
  <li>Module 2: Taxonomic Classification [Read-Based]</li>
  <li>Module 3: Assembly</li>
  <li>Module 4: Quality assessment of assembly</li>
  <li>Module 5: Functional Classification [Read-Based]</li>
</ul>


### Module 1: Reads quality check
trim-galore
```
conda install -c bioconda trim-galore
```

### Module 2: 
Kaiju (Taxonomic classification [Read-based])
```
conda install -c bioconda kaiju
```

### Module 3
metaSPAdes (Assembly)
```
conda install -c bioconda spades
```

Megahit
```
conda install -c bioconda megahit
```

### Module 4
MetaQuast - Quality Assessment Tool for Genome Assemblies
```
conda install -c bioconda quast
```

### Module 5
mifaser (Functional classification [Read-based])
```
conda install -c bioconda diamond
pip install mifaser
```
