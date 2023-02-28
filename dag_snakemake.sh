#!/bin/bash
#

snakefile=$1

snakemake -s $snakefile --dag | dot -Tpdf > dag.pdf

