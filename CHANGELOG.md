<!--
Note: this file is automatically synced to docs/source/lastupdate.md
on the gh-pages branch every time the docs site is rebuilt.
-->

# Change Log
Major changes will be documented in this file.


## Version 1.5.1 (Aug 31, 2026)
### Added
- Add module `assembly_redox_metal_indexes` for index computation at assembly level using KOfam-scan
- Add module `mags_redox_metal_indexes` for index computation at binning level using KOfam-scan
### Changed

### Fixed


## Version 1.4.3 (May 28, 2026)
### Added

### Changed

### Fixed
- minor fix on gathering kaiju and redox metabolic indexes


## Version 1.4.3 (May 29, 2026)
### Added

### Changed

### Fixed
- Fixed `mags_hmmsearch` gather output to standard presence/absence gene matrix
- Fixed gathering logic in `kaiju`,`funprofiler`,`redox_metal_indexes_rb`,`mifaser`


## Version 1.4.2 (May 28, 2026)
### Added

### Changed
- Changed variable type in `metal_indexes_rb` for R downstream analysis
### Fixed


## Version 1.4.1 (May 19, 2026)
### Added
- Add gather option to `kofam_scan` package at the bin-based stream
### Changed

### Fixed


## Version 1.3.6 (Mar 26, 2026)
### Added

### Changed
- Renamed gather func & inner function for consistency
- Renaming smk output files & 2nd rule in redox_metal_plasticity_index module
### Fixed


## Version 1.3.5 (Mar 25, 2026)
### Added

### Changed
- Renamed module `metal_indexes_rb` to `redox_metal_indexes` and tool from `rmi_rpi_indexes` to `redox_metal_plasticity_index`
- Renaming rules, functions according to new namings, and variables
### Fixed


## Version 1.3.4 (Mar 24, 2026)
### Added

### Changed

### Fixed
- Minor fix to nans in NO_metal exception
- Minor fix to incosistent args namings


## Version 1.3.3 (Mar 19, 2026)
### Added

### Changed

### Fixed
- Fix rpi to account for unique Metal pairs


## Version 1.3.2 (Mar 13, 2026)
### Added
- Added possibility to subfolder in get_sample_results
### Changed
- Renamed gather function `metal_index_rb` to `rmi_rpi_indexes` & change in gm_gather
- Removed cat raw_reads lanes in gm_setup & Change in `--move_and_rename` args flag
### Fixed
- Fix typo on gather_mags_recognizer
- Fix issue related to gather_rmi_rpi_indexes


## Version 1.3.1 (Mar 06, 2026)
### Added

### Changed
- Removed DRAM from mags_functional_annotation module
### Fixed
- Env parameter for snakefile (BBmap & Bowtie2 shrinked)


## Version 1.3.0 (Feb 18, 2026)
### Added
- Add new module for redox-metabolix & palsticity index computation
### Changed

### Fixed
- Minor fix on single_sample GNU_parallel sh script


## Version 1.2.5 (Dec 9, 2025)
### Added

### Changed
- Changed `-l` option in `kaiju2table` command for complete taxonomic information

### Fixed


## Version 1.2.4 (Dec 1, 2025)
### Added
- Add thread limit to `funprofiler` snakefile, to hamper sourmash threads parlalelization
### Changed
- Removed `--unit` flag from gather command to rely on samples retrieved directly from gmsetup.yaml
- Minor refactors in gathering scripts to accomodate flag change
### Fixed


## Version 1.2.3 (Nov 25, 2025)
### Added
- Added new optional flag `--conda_frontend` to the `prerun` command, allowing users to specify which Conda frontend Snakemake should use (`conda` or `mamba`).

### Changed

### Fixed


## Version 1.2.2 (Nov 19, 2025)
### Added

### Changed

### Fixed
- Fixed license specification in toml file and `geomosaic --version` command

## Version 1.2.1 (Nov 19, 2025)
### Added
- Added new required flag `--source` to the `prerun` command to indicate which previous Geomosaic command was executed: `unit` or `workflow`. This allows Geomosaic to select the correct configuration file for execution.
### Changed
- Removed the optional `--unit` flag from the `prerun` command.
### Fixed

## Version 1.1.4 (Nov 18, 2025)
### Added
- Added fmh-funprofiler for functional annotation with pre-defined KO database (Module: `func_classification_rb`)
### Changed

### Fixed

## Version 1.1.3 (Jan 8, 2025)
### Added
 
### Changed
 
### Fixed
- Fixed ARGs-OAP with custom db (Module: `func_classification_rb`)


## Version 1.1.1 (Dec 27, 2024)
### Added
- Added ARGs-OAP Tool (Module: `func_classification_rb`) for read based quantification with custom database  as alternative to mi-faser. For detailed documentation please refer to: [https://github.com/xinehc/args_oap](https://github.com/xinehc/args_oap)
 
### Changed
 
### Fixed

<br>

## Version 1.1.0 (Sep 25, 2024)
 
First Major Release
