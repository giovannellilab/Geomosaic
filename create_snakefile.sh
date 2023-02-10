#!/bin/bash

input="raw_metagenomes/example"

output="raw_metagenomes/output_example"

for file in ${input}/*_R1*.gz; do
    path_file=$(dirname $(readlink -f $file ))
    sample_file=$(basename $file)

    read_prefix=${sample_file%_R1*}
    read_suffix=${sample_file#*_R1}
    
    IFS='.' read rawsample fastqext gzext <<< ${sample_file}

    prefix=${rawsample%_R1*}
    suffix=${rawsample#*_R1}

    sample="$prefix$suffix"    

    mkdir -p ${output}/$sample

    ln -s -T $path_file/${read_prefix}_R1${read_suffix} ${output}/$sample/R1.fastq.gz
    ln -s -T $path_file/${read_prefix}_R2${read_suffix} ${output}/$sample/R2.fastq.gz

done

all_samples=$(ls -1 $output | sed "s/^/'/;s/$/',/")

printf -v joined '%s' "${all_samples[@]}"

printf "SAMPLES=[$joined]\n\nWDIR=\"$output\"\n\n" | cat - Snakefile > temp && mv temp Snakefile
