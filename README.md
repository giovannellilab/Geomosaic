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

<ul>
  <li>Pre-processing</li>
  <li>Functional Classification [Read-based]</li>
  <li>Taxonomic Classification [Read-based]</li>
  <li>Assembly</li>
  <li>Assembly Evaluation: Quality Check</li>
  <li>Assembly Evaluation: Read Mapping</li>
  <li>Gene Coverage</li>
  <li>ORF Prediction</li>
  <li>Binning</li>
  <li>Binning Quality Assessment</li>
</ul>

### Pre-processing
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
- MetaBat2

### Binning Quality Assessment
- CheckM

### Functional classification [Read-Based]
- mi-faser
- MetaPhlAn

### Taxonomic classification [Read-Based]
- Kaiju

### ORF Prediction
- Prodigal

### Gene Coverage
HMMSearch on prodigal results and pileup.sh (from BBMap tool) to get the coverage per ORF
- HMMSearch-Pileup(BBmap)