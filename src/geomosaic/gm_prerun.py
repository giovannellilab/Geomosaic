import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_NOTE, GEOMOSAIC_PROMPT
from subprocess import check_call
from geomosaic._slurm_templates import exectype_slurm
from geomosaic._gnuparallel_templates import exectype_gnuparalllel


def geo_prerun(args):
    setup_file  = args.setup_file
    unit        = args.unit
    exectype    = args.exec_type

    with open(setup_file) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    geomosaic_dir = geomosaic_setup["GEOMOSAIC_WDIR"]
    geomosaic_samples = geomosaic_setup["SAMPLES"]

    name_snakefile = "Snakefile_unit.smk" if unit else "Snakefile.smk"
    exists_extdb = check_extdb_snakefile(geomosaic_dir, unit)
    gm_snakefile = str(os.path.join(geomosaic_dir, name_snakefile))
    
    if exectype == "slurm":
        output_script, sw, \
            extdb_output_script, extdb, \
                singleSample_output_script, singleSample, \
                    list_sample_output = exectype_slurm(args, geomosaic_samples, geomosaic_dir, gm_snakefile, unit)

        with open(list_sample_output, "wt") as fl:
            for s in geomosaic_setup["SAMPLES"]:
                fl.write(f"{s}\n")

        with open(output_script, "wt") as fd:
            fd.write(sw)

        if exists_extdb:
            with open(extdb_output_script, "wt") as fd:
                fd.write(extdb)
        
        with open(singleSample_output_script, "wt") as fd:
            fd.write(singleSample)
    
        show_slurm_message(exists_extdb, extdb_output_script, output_script, singleSample_output_script, list_sample_output)
    
    else:
        output_script, sw, \
            extdb_output_script, extdb, \
                list_sample_output = exectype_gnuparalllel(args, geomosaic_dir, gm_snakefile, unit)

        with open(list_sample_output, "wt") as fl:
            for s in geomosaic_setup["SAMPLES"]:
                fl.write(f"{s}\n")

        with open(output_script, "wt") as fd:
            fd.write(sw)

        with open(extdb_output_script, "wt") as fd:
            fd.write(extdb)
        
        prompt1 = GEOMOSAIC_PROMPT(f"$ bash {extdb_output_script}")
        prompt2 = GEOMOSAIC_PROMPT(f"$ bash {output_script}")
        print(f"\n{GEOMOSAIC_NOTE}: The following draft scripts for GNU Parallel execution are created (along with file containing the samples list):\n{output_script}\n{extdb_output_script}\n{list_sample_output}")
        print(f"\nThese script can be considered minimal for GNU Parallel.\nFeel free to modify them to add more complex codes. More details can be retrieved to official GNU Parallel Documentation.")
        print(f"\n{GEOMOSAIC_NOTE}: Since your using GNU Parallel, you should set the number of jobs to execute in parallel taking into account the number of cpus that you can use.\nFor instance, if 36 cores are available you can open the following file\n{GEOMOSAIC_PROMPT(output_script)}\n\nand modify the following variables\n{GEOMOSAIC_PROMPT('n_jobs_in_parallel=4')}\n{GEOMOSAIC_PROMPT('threads_per_job=9')}.")
        print(f"\n{GEOMOSAIC_NOTE}: So now you are ready to go!\nYour first step should be to setup the required databases of your pipeline, by executing:\n{prompt1}\n\nonce it is finished, you can execute the real pipeline:\n{prompt2}")
    
    print(f"\n{GEOMOSAIC_PROCESS}: Installing all the conda environments of your workflow/unit. This may take a while...\n", end="", flush=True)
    envinstall(geomosaic_dir, gm_snakefile, unit)


def envinstall(geomosaic_wdir, gm_snakefile, unit):
    path_extdb_folder = os.path.join(geomosaic_wdir, "gm_external_db")

    filename = "config_unit.yaml" if unit else "config.yaml"
    config_file = os.path.join(geomosaic_wdir, filename)

    # CHECK CONFIG FILE EXISTS
    if not os.path.isfile(config_file):
        print(f"\n{GEOMOSAIC_ERROR}: '{filename}' does not exists in the Geomosaic WDIR: {geomosaic_wdir}")
        exit(1)
    
    # OPEN CONFIG FILE
    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    extdbs = config["EXT_DB"]
    
    # CREATE TEST FOLDERS
    for k, path in extdbs.items():
        extdb_dir = path.split("/")[-1]
        check_call(f"(cd {path_extdb_folder} && mkdir -p {extdb_dir})", shell=True)
    
    check_call(["snakemake", "--use-conda", "--conda-create-envs-only", "--cores", "1", "-s", gm_snakefile])

    # REMOVE TEST FOLDERS
    for k, path in extdbs.items():
        extdb_dir = path.split("/")[-1]
        try:
            os.rmdir(path)
        except OSError:
            pass

    print(GEOMOSAIC_OK)


def show_slurm_message(exists_extdb, extdb_output_script, output_script, singleSample_output_script, list_sample_output):
    if exists_extdb:
        existing_files = [output_script, extdb_output_script, singleSample_output_script, list_sample_output]
        prompt1 = GEOMOSAIC_PROMPT(f"$ sbatch {extdb_output_script}")
        prompt2 = GEOMOSAIC_PROMPT(f"$ sbatch {output_script}")
        prompt3 = GEOMOSAIC_PROMPT(f"$ sbatch {singleSample_output_script} MYSAMPLE")

        steps = [
            (f"{GEOMOSAIC_PROMPT('STEP 1)')}: setup the required databases of your pipeline, by executing:", prompt1),
            (f"{GEOMOSAIC_PROMPT('STEP 2)')}: once it is finished, you can execute the real pipeline:", prompt2),
            (f"{GEOMOSAIC_PROMPT('EVENTUALLY)')}: if you need to execute your workflow/unit just for one sample you can execute the following script through sbatch (specifying your sample name of interest):", prompt3),
        ]
    else:
        existing_files = [output_script, singleSample_output_script, list_sample_output]
        prompt1 = GEOMOSAIC_PROMPT(f"$ sbatch {extdb_output_script}")
        prompt2 = GEOMOSAIC_PROMPT(f"$ sbatch {output_script}")
        prompt3 = GEOMOSAIC_PROMPT(f"$ sbatch {singleSample_output_script} MYSAMPLE")

        steps = [
            (f"{GEOMOSAIC_PROMPT('STEP 1)')}: you can execute the real pipeline due to the fact that you don't need to setup any database:", prompt2),
            (f"{GEOMOSAIC_PROMPT('EVENTUALLY)')}: if you need to execute your workflow/unit just for one sample you can execute the following script through sbatch (specifying your sample name of interest):", prompt3),
        ]

    list_files = "\n\t- ".join(existing_files)

    merging_steps = ""
    for descr, cmd in steps:
        merging_steps += descr
        merging_steps += f"\n\t{cmd}\n\n"
    
    print(f"\n{GEOMOSAIC_NOTE}: The following draft scripts for slurm execution were created (along with file containing the samples list):\n\t- {list_files}")
    print(f"\nThese script can be considered minimal for SLURM. If you need you can modify them to add more SBATCH information.\nMore details can be retrieved to official SLURM Documentation.")
    print(f"\n{GEOMOSAIC_NOTE}: So now you are ready to go!\n\n{merging_steps}")


# dag_image = os.path.join(geomosaic_dir, "dag.pdf")
    # subprocess.check_call(f"snakemake -s {snakefile_filename} --rulegraph | dot -Tpdf > {dag_image}", shell=True)


def check_extdb_snakefile(geomosaic_wdir, unit):
    filename = "config_unit.yaml" if unit else "config.yaml"
    config_file = os.path.join(geomosaic_wdir, filename)

    # CHECK CONFIG FILE EXISTS
    if not os.path.isfile(config_file):
        print(f"\n{GEOMOSAIC_ERROR}: '{filename}' does not exists in the Geomosaic WDIR: {geomosaic_wdir}")
        exit(1)
    
    # OPEN CONFIG FILE
    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
    
    extdbs = config["EXT_DB"]

    if len(extdbs.items()) == 0:
        return False
    else:
        return True
