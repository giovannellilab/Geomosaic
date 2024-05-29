import os
from subprocess import check_call
from geomosaic._utils import GEOMOSAIC_PROCESS
from geomosaic._slurm_templates import update_threads


def exectype_gnuparalllel(args, geomosaic_dir, gm_snakefile, unit, geomosaic_condaenvs_folder):
    temp_threads = args.threads
    n_jobs = args.n_jobs
    path_geomosaic_snakefile = gm_snakefile
    unit_suffix = "_unit" if unit else ""
    output_script = os.path.abspath(f"parallel{unit_suffix}_geomosaic.sh")
    extdb_output_script = os.path.abspath("parallel_extdb_geomosaic.sh")
    singleSample_output_script = os.path.abspath(f"parallel{unit_suffix}_singleSample_geomosaic.sh")
    list_sample_output = os.path.abspath("list_samples.txt")
    
    if args.folder_logs is not None:
        folder_logs = os.path.abspath(args.folder_logs)

        if not os.path.isdir(folder_logs):
            print(f"{GEOMOSAIC_PROCESS}: Creating the specified folder logs: '{folder_logs}'")
            check_call(["mkdir", "-p", folder_logs])
        
        gnuparallel_logs = str(os.path.join(folder_logs, "{}.log"))
    else:
        gnuparallel_logs = "{}.log"
    
    threads = update_threads(unit, geomosaic_dir, temp_threads)

    sw = gnuparallel_workflow.format(
        threads = threads, 
        n_jobs=n_jobs,
        path_geomosaic_snakefile = path_geomosaic_snakefile,
        path_list_sample = list_sample_output,
        gnuparallel_logs = gnuparallel_logs,
        geomosaic_condaenvs_folder = geomosaic_condaenvs_folder
    )

    extdb = gnuparallel_extdb.format(
        path_extdb_snakefile = str(os.path.join(geomosaic_dir, "Snakefile_extdb.smk")),
        geomosaic_condaenvs_folder = geomosaic_condaenvs_folder
    )

    singleSample = gnuparallel_singleSample.format(
        threads = threads,
        path_geomosaic_snakefile = path_geomosaic_snakefile,
        gnuparallel_logs = gnuparallel_logs,
        geomosaic_condaenvs_folder = geomosaic_condaenvs_folder
    )
    
    return output_script, sw, extdb_output_script, extdb, singleSample_output_script, singleSample, list_sample_output


gnuparallel_workflow="""
#!/bin/bash

#
# Created with Geomosaic
#

n_jobs_in_parallel={n_jobs}
threads_per_job={threads}


cat {path_list_sample} | parallel -j $n_jobs_in_parallel \\
    snakemake --use-conda --conda-prefix {geomosaic_condaenvs_folder} \\
    --cores $threads_per_job \\
    -s {path_geomosaic_snakefile} \\
    --config SAMPLES={{}} ">" {gnuparallel_logs} 2>&1

"""

gnuparallel_extdb="""
#!/bin/bash

#
# Created with Geomosaic
#


snakemake --use-conda --conda-prefix {geomosaic_condaenvs_folder} --cores 9 -s {path_extdb_snakefile}

"""

gnuparallel_singleSample="""
#!/bin/bash

#
# Created with Geomosaic
#

if [ -z $1 ] ; then
    echo 'No argument "SAMPLE" supplied.'
    echo 'Execution type of this script: bash parallel_simpleSample_geomosaic MYSAMPLE'
    echo 'Exit.'
    exit 1
fi

single_sample=$1

echo "SAMPLE: $single_sample"

threads_per_job={threads}

parallel -j 1 \\
    snakemake --use-conda --conda-prefix {geomosaic_condaenvs_folder} \\
    --cores $threads_per_job \\
    -s {path_geomosaic_snakefile} \\
    --config SAMPLES=$single_sample ">" {gnuparallel_logs} 2>&1

"""
