#!/bin/bash
#



helpFunction()
{
    echo ""
    echo "GeoMosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis"
    echo ""
    echo "Usage: $0 -d <rawreads_directory> -w <working_dir> -s <sample_table> "
    echo -e "\t-d Path to the directory containing raw reads (fastq.gz files)"
    echo -e "\t-w Path to the working directory for geomosaic"
    echo -e "\t-s Sample table"
    exit 1 # Exit script after printing help
}

while getopts "d:w:s:" opt
do
    case "$opt" in
        d ) directory="$OPTARG" ;;
        w ) working_dir="$OPTARG" ;;
        s ) sample_table="$OPTARG" ;;
        ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
    esac
done

# Print helpFunction in case parameters are empty
if [ -z "$directory" ] || [ -z "$working_dir" ] || [ -z "$sample_table" ]
then
    echo "Some or all of the parameters are empty";
    helpFunction
fi

python3 scripts/user_choices.py -d $directory -w $working_dir -s $sample_table

./dag_snakefile.sh Snakefile

snakemake --use-conda --cores 20
