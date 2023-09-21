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
  <li>Binning De-replication</li>
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
- quast

### Assembly Evaluation: Read Mapping
- BBmap

### Binning
- MaxBin2 + MetaBat2 + Concoct

### Binning De-replication
- DAS_Tool


### Binning Quality Assessment
- CheckM

### Functional classification [Read-Based]
- mi-faser

### Taxonomic classification [Read-Based]
- Kaiju
- MetaPhlAn

### ORF Prediction
- Prodigal

### Gene Coverage
HMMSearch on prodigal results and pileup.sh (from BBMap tool) to get the coverage per ORF
- HMMSearch-Pileup(BBmap)