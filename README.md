# GeoMosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis

The first step is to install the conda environment of Geomosaic.
```
conda env create -f environment.yaml
```
Then activate it
```
conda activate geomosaic
```

## Integrated Modules

This pipeline is organized in modules:
<ul>
  <li>Pre-processing</li>
  <li>Assembly</li>
  <li>Assembly Evaluation: Quality Check</li>
  <li>Assembly Evaluation: Read Mapping</li>
  <li>Binning</li>
  <li>Functional Classification [Read-based]</li>
  <li>Taxonomic Classification [Read-based]</li>
</ul>


### Pre-processing
Integrated modules:
- fastp
- trim-galore
- trimmomatic

### Assembly: 
- Metaspades
- MegaHit

### Assembly Evaluation: Quality Check
- MetaQuast

### Assembly Evaluation: Read Mapping
- BBmap

### Binning
- MaxBin2

### Functional classification [Read-Based]
- mi-faser

### Taxonomic classification [Read-Based]
- Kaiju
