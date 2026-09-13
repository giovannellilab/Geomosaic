
![Geomosaic](images/geomosaic_logo_multicolor_300dpi.png)

<br>

[![forthebadge](https://forthebadge.com/images/badges/powered-by-coffee.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-science.svg)](https://forthebadge.com)

[![giovannellilab](https://img.shields.io/badge/BY-Giovannelli_Lab-blue)](https://www.donatogiovannelli.com)
[![funded-by-erc](https://img.shields.io/badge/Funded%20by-ERC-ff6400.svg)](https://erc.europa.eu/homepage)
[![project-coevolve](https://img.shields.io/badge/Project-ERC%20CoEvolve-000fa9.svg)](https://www.coevolve.eu/)

[![DOI](https://zenodo.org/badge/603053899.svg)](https://doi.org/10.5281/zenodo.11036349)

<br>

__Geomosaic__ is  a modular framework that integrates complementary analytical representations of metagenomic data, from reads to genomes, within a single scalable, customizable, and reproducible workflow. Built on a graph-based architecture implemented in Snakemake, Geomosaic enables users to construct complete end-to-end workflows or execute individual analytical modules while selecting among interchangeable software packages. The framework supports read preprocessing, quality control, taxonomic and functional profiling, assembly, genome reconstruction, genome-resolved annotation, custom HMM-based analyses, and automated downstream result aggregation. Automatic generation of execution scripts, modular workflows, and multiple analysis entry points make Geomosaic accessible to researchers approaching metagenomic analyses for the first time, while providing the flexibility and control required by expert users. Native support for HPC environments enables efficient analysis of datasets ranging from individual projects to large-scale metagenomic surveys.

Full Documentation available at: [giovannellilab.github.io/Geomosaic](https://giovannellilab.github.io/Geomosaic)


# Citation

If you used __GEOMOSAIC__ for your analysis, please cite:

> Davide Corso, Edoardo Taccaliti, Bernardo Barosa, and Donato Giovannelli. **Geomosaic: a flexible bioinformatics platform integrating complementary metagenomic analyses from sequencing reads to genomes.** *bioRxiv preprint (2026)*. doi: [10.64898/2026.09.05.749574](https://doi.org/10.64898/2026.09.05.749574).

<details>
<summary><b>BibTeX entry</b> (click to expand)</summary>

```bibtex
@article{corso2026geomosaic,
  title     = {Geomosaic: a flexible bioinformatics platform integrating complementary metagenomic analyses from sequencing reads to genomes},
  author    = {Corso, Davide and Taccaliti, Edoardo and Barosa, Bernardo and Giovannelli, Donato},
  journal   = {bioRxiv},
  year      = {2026},
  doi       = {10.64898/2026.09.05.749574},
  url       = {https://doi.org/10.64898/2026.09.05.749574},
  note      = {Preprint}
}
```

</details>

> **Note on modular tools:** Geomosaic wraps multiple third-party tools (e.g., assemblers, profilers, and binners). When reporting your results, please also cite the specific software modules executed by your workflow.