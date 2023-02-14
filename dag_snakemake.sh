#!/bin/bash
#


snakemake --dag | dot -Tpdf > dag.pdf

