import os
from subprocess import check_call
from geomosaic._utils import GEOMOSAIC_PROCESS
from geomosaic._slurm_templates import update_threads


def exectype_gnuparalllel(args, geomosaic_dir, gm_snakefile, unit):
    threads = args.threads
    n_jobs = args.n_jobs
    path_geomosaic_snakefile = gm_snakefile
    output_script = os.path.abspath("parallel_geomosaic.sh") if args.output_script is None else os.path.abspath(args.output_script)
    extdb_output_script = os.path.abspath("parallel_extdb_geomosaic.sh") if args.extdb_output_script is None else os.path.abspath(args.extdb_output_script)
    list_sample_output = os.path.abspath(args.list_sample_output)
    
    if args.folder_logs is not None:
        folder_logs = os.path.abspath(args.folder_logs)

        if not os.path.isdir(folder_logs):
            print(f"{GEOMOSAIC_PROCESS}: Creating the specified folder logs: 'mkdir -p {folder_logs}'")
            check_call(["mkdir", "-p", folder_logs])
        
        gnuparallel_logs = str(os.path.join(folder_logs, "{}.log"))
    else:
        gnuparallel_logs = "{}.log"
    
    update_threads(unit, geomosaic_dir, threads)

    sw = gnuparallel_workflow.format(
        threads = threads, 
        n_jobs=n_jobs,
        path_geomosaic_snakefile = path_geomosaic_snakefile,
        path_list_sample = list_sample_output,
        gnuparallel_logs = gnuparallel_logs,
    )

    extdb = gnuparallel_extdb.format(
        path_extdb_snakefile = str(os.path.join(geomosaic_dir, "Snakefile_extdb.smk"))
    )
    
    return output_script, sw, extdb_output_script, extdb, list_sample_output


gnuparallel_workflow="""
#!/bin/bash

#
# Created with Geomosaic
#

n_jobs_in_parallel={n_jobs}
threads_per_job={threads}


cat {path_list_sample} | parallel -j $n_jobs_in_parallel \\
    snakemake --use-conda \\
    --cores $threads_per_job \\
    -s {path_geomosaic_snakefile} \\
    --config SAMPLES={{}} ">" {gnuparallel_logs} 2>&1

"""

gnuparallel_extdb="""
#!/bin/bash

#
# Created with Geomosaic
#


snakemake --use-conda --cores 4 -s {path_extdb_snakefile}

"""
