import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_NOTE, GEOMOSAIC_PROMPT
from subprocess import check_call
from geomosaic._slurm_templates import exectype_slurm
from geomosaic._gnuparallel_templates import exectype_gnuparalllel
from geomosaic._dummy_snakefile import create_dummy_snakefile


def geo_prerun(args):
    gmsetup_file    = args.setup_file
    unit            = args.unit
    exectype        = args.exec_type
    ignore_samples  = args.ignore_samples

    with open(gmsetup_file) as file:
        gmsetup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in gmsetup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in gmsetup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert "GM_CONDA_ENVS" in gmsetup, f"\n{GEOMOSAIC_ERROR}: geomosaic conda envs directory must be provided with the key 'GM_CONDA_ENVS'"
    
    assert os.path.isdir(gmsetup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    geomosaic_wdir = gmsetup["GEOMOSAIC_WDIR"]
    temp_geomosaic_samples = gmsetup["SAMPLES"]
    geomosaic_condaenvs_folder = gmsetup["GM_CONDA_ENVS"]
    jobname = gmsetup["PROJECT_NAME"][:8]

    name_snakefile = "Snakefile_unit.smk" if unit else "Snakefile.smk"
    exists_extdb = check_extdb_snakefile(geomosaic_wdir, unit)
    gm_snakefile = str(os.path.join(geomosaic_wdir, name_snakefile))

    geomosaic_samples = consider_ignored_samples(temp_geomosaic_samples, ignore_samples)

    if exectype == "slurm":
        output_script, sw, \
            extdb_output_script, extdb, \
                singleSample_output_script, singleSample, \
                    list_sample_output = exectype_slurm(args, geomosaic_samples, geomosaic_wdir, 
                                                        gm_snakefile, unit, 
                                                        geomosaic_condaenvs_folder, jobname)

        with open(list_sample_output, "wt") as fl:
            for s in geomosaic_samples:
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
                singleSample_output_script, singleSample, \
                    list_sample_output = exectype_gnuparalllel(args, geomosaic_wdir, gm_snakefile, unit, geomosaic_condaenvs_folder)

        with open(list_sample_output, "wt") as fl:
            for s in geomosaic_samples:
                fl.write(f"{s}\n")

        with open(output_script, "wt") as fd:
            fd.write(sw)

        with open(extdb_output_script, "wt") as fd:
            fd.write(extdb)
        
        with open(singleSample_output_script, "wt") as fd:
            fd.write(singleSample)
        
        show_gnuparallel_message(exists_extdb, extdb_output_script, output_script, singleSample_output_script, list_sample_output)
    
    print(f"\n{GEOMOSAIC_PROCESS}: Installing all the conda environments of your workflow/unit. This may take a while...\n", end="", flush=True)
    envinstall(geomosaic_wdir, geomosaic_condaenvs_folder,  unit)


def envinstall(geomosaic_wdir, geomosaic_condaenvs_folder,  unit):
    filename = "config_unit.yaml" if unit else "config.yaml"
    config_file = os.path.join(geomosaic_wdir, filename)

    # CHECK CONFIG FILE EXISTS
    if not os.path.isfile(config_file):
        print(f"\n{GEOMOSAIC_ERROR}: '{filename}' does not exists in the Geomosaic WDIR: {geomosaic_wdir}")
        exit(1)

    dummy_filename = os.path.join(geomosaic_wdir, "dummy_snakefile.smk")
    create_dummy_snakefile(geomosaic_wdir, config_file, dummy_filename)
    check_call(["snakemake", "--use-conda", "--conda-prefix", geomosaic_condaenvs_folder, "--conda-create-envs-only", "--cores", "1", "-s", dummy_filename])
    os.remove(dummy_filename)

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


def show_gnuparallel_message(exists_extdb, extdb_output_script, output_script, singleSample_output_script, list_sample_output):
    if exists_extdb:
        existing_files = [output_script, extdb_output_script, singleSample_output_script, list_sample_output]
        prompt1 = GEOMOSAIC_PROMPT(f"$ bash {extdb_output_script}")
        prompt2 = GEOMOSAIC_PROMPT(f"$ bash {output_script}")
        prompt3 = GEOMOSAIC_PROMPT(f"$ bash {singleSample_output_script} MYSAMPLE")

        steps = [
            (f"{GEOMOSAIC_PROMPT('STEP 1)')}: setup the required databases of your pipeline, by executing:", prompt1),
            (f"{GEOMOSAIC_PROMPT('STEP 2)')}: once it is finished, you can execute the real pipeline:", prompt2),
            (f"{GEOMOSAIC_PROMPT('EVENTUALLY)')}: if you need to execute your workflow/unit just for one sample you can execute the following script through bash (specifying your sample name of interest):", prompt3),
        ]
    else:
        existing_files = [output_script, singleSample_output_script, list_sample_output]
        prompt1 = GEOMOSAIC_PROMPT(f"$ bash {extdb_output_script}")
        prompt2 = GEOMOSAIC_PROMPT(f"$ bash {output_script}")
        prompt3 = GEOMOSAIC_PROMPT(f"$ bash {singleSample_output_script} MYSAMPLE")

        steps = [
            (f"{GEOMOSAIC_PROMPT('STEP 1)')}: you can execute the real pipeline due to the fact that you don't need to setup any database:", prompt2),
            (f"{GEOMOSAIC_PROMPT('EVENTUALLY)')}: if you need to execute your workflow/unit just for one sample you can execute the following script through bash (specifying your sample name of interest):", prompt3),
        ]

    list_files = "\n\t- ".join(existing_files)

    merging_steps = ""
    for descr, cmd in steps:
        merging_steps += descr
        merging_steps += f"\n\t{cmd}\n\n"
    
    print(f"\n{GEOMOSAIC_NOTE}: The following draft scripts for GNU Parallel execution were created (along with file containing the samples list):\n\t- {list_files}")
    print(f"\nThese script can be considered minimal for GNU Parallel. Feel free to modify them to add more complex codes.\nMore details can be retrieved to official GNU Parallel Documentation.")
    print(f"\n{GEOMOSAIC_NOTE}: Since your using GNU Parallel, you should set the number of jobs to execute in parallel taking into account the number of cpus that you can use.\nFor instance, if 36 cores are available you can open the following file\n{GEOMOSAIC_PROMPT(output_script)}\n\nand modify the following variables\n{GEOMOSAIC_PROMPT('n_jobs_in_parallel=4')}\n{GEOMOSAIC_PROMPT('threads_per_job=9')}.")
    print(f"\n{GEOMOSAIC_NOTE}: So now you are ready to go!\n\n{merging_steps}")


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


def consider_ignored_samples(gmsetup_samples, user_ignore_samples):
    if user_ignore_samples is not None:
        ignore_samples = list(user_ignore_samples)
        geomosaic_samples = []
        ignoring = []
        for x in gmsetup_samples:
            if x in ignore_samples:
                ignoring.append(x)
            else:
                geomosaic_samples.append(x)
        if len(ignoring) == 0:
            print(f"{GEOMOSAIC_ERROR}: Seems that you have put sample/s to ignore however Geomosaic didn't retrieve any samples you provided from the gmsetup.yaml")
            exit(1)
        elif len(ignoring) == len(ignore_samples):
            print(f"{GEOMOSAIC_NOTE}: ignoring the following samples: {str(','.join(ignoring))}")
        else:
            print(f"{GEOMOSAIC_NOTE}: Seems that Geomosaic recognized a lower number of samples than provided. Try to review them.")
        
    else:
        geomosaic_samples = gmsetup_samples

    return geomosaic_samples
