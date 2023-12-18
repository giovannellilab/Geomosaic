slurm_workflow = """
#!/bin/bash

#SBATCH --job-name="Geomosaic"
#SBATCH --time=96:00:00
#SBATCH --cpus-per-task={threads}
#SBATCH --mem={memory}G
#SBATCH --array=1-{samples_number}
{slurm_logs}
{partition}
{mail_type}
{mail_user}

#
# Created with Geomosaic
# 


single_sample="$(tail -n +$SLURM_ARRAY_TASK_ID {path_list_sample} | head -n1)"


snakemake --use-conda --cores {threads} --config SAMPLES=$single_sample -s {path_geomosaic_snakefile}
"""

slurm_extdb = """
#!/bin/bash

#SBATCH --job-name="Extdb_GM"
#SBATCH --time=96:00:00
#SBATCH --cpus-per-task=7
#SBATCH --mem={memory}G
{slurm_logs}
{partition}
{mail_type}
{mail_user}

#
# Created with Geomosaic
# 


snakemake --use-conda --cores 7 -s {path_extdb_snakefile}
"""
