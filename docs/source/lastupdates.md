# Last Updates

Major changes will be documented in this page.

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

## Version 1.1.3 (Jan 8, 2025)
### Added
 
### Changed
 
### Fixed
- Fixed ARGs-OAP with custom db (Module: `func_classification_rb`)


## Version 1.1.1 (Dec 27, 2024)
### Added
- Added ARGs-OAP Tool (Module: `func_classification_rb`) for read based quantification with custom database as alternative to mi-faser. For detailed documentation please refer to: [https://github.com/xinehc/args_oap](https://github.com/xinehc/args_oap)

For detailed information on how to use this tool on Geomosaic: [Tips on specific tool](tips/specifictools.md#args-oap-with-custom-db)
 
### Changed
 
### Fixed

<br>

## Version 1.1.0 (Sep 25, 2024)
 
First Major Release