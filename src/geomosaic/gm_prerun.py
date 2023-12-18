import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_NOTE, GEOMOSAIC_PROMPT
from subprocess import check_call
from geomosaic._slurm_templates import slurm_workflow, slurm_extdb


def geo_prerun(args):
    print(f"{GEOMOSAIC_PROCESS}: Installing all the conda environments of your workflow/unit. This may take a while...\n", end="", flush=True)
    setup_file  = args.setup_file
    unit        = args.unit
    slurm       = args.slurm

    with open(setup_file) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    geomosaic_dir = geomosaic_setup["GEOMOSAIC_WDIR"]

    name_snakefile = "Snakefile_unit.smk" if unit else "Snakefile.smk"
    gm_snakefile = str(os.path.join(geomosaic_dir, name_snakefile))

    if slurm:
        threads = args.threads
        memory = args.memory
        partition = "" if args.partition is None else f"#SBATCH --partition={args.partition}"
        mail_type = "" if args.mail_type is None else f"#SBATCH --mail-type={args.mail_type}"
        mail_user = "" if args.mail_user is None else f"#SBATCH --mail-user={args.mail_user}"
        samples_number = len(geomosaic_setup["SAMPLES"])
        path_geomosaic_snakefile = gm_snakefile
        output_script = os.path.abspath(args.output_script)
        extdb_output_script = os.path.abspath(args.extdb_output_script)
        list_sample_output = os.path.abspath(args.list_sample_output)
        
        if args.folder_logs is not None:
            folder_logs = os.path.abspath(args.folder_logs)

            if not os.path.isdir(folder_logs):
                print(f"{GEOMOSAIC_PROCESS}: Creating the specified folder logs: 'mkdir -p {folder_logs}'")
                check_call(["mkdir", "-p", folder_logs])
            
            slurm_logs = "#SBATCH --output=" +os.path.join(folder_logs, "slurm-%A_%a.out")
        else:
            slurm_logs = ""
        
        update_threads(unit, geomosaic_dir, threads)

        sw = slurm_workflow.format(
            threads = threads, 
            memory = memory, 
            partition = partition, 
            samples_number = samples_number,
            path_geomosaic_snakefile = path_geomosaic_snakefile,
            path_list_sample = list_sample_output,
            mail_type = mail_type,
            mail_user = mail_user,
            slurm_logs = slurm_logs,
        )

        extdb = slurm_extdb.format(
            memory = memory,
            slurm_logs = slurm_logs,
            partition = partition,
            mail_type = mail_type,
            mail_user = mail_user,
            path_extdb_snakefile = str(os.path.join(geomosaic_dir, "Snakemake_extdb.smk"))
        )

        with open(list_sample_output, "wt") as fl:
            for s in geomosaic_setup["SAMPLES"]:
                fl.write(f"{s}\n")

        with open(output_script, "wt") as fd:
            fd.write(sw)

        with open(extdb_output_script, "wt") as fd:
            fd.write(extdb)
    
    envinstall(geomosaic_dir, gm_snakefile, unit)

    if slurm:
        prompt1 = GEOMOSAIC_PROMPT(f"$ sbatch {extdb_output_script}")
        prompt2 = GEOMOSAIC_PROMPT(f"$ sbatch {output_script}")
        print(f"\n{GEOMOSAIC_NOTE}: The following draft scripts for slurm execution were created (along with file containing the samples list):\n{output_script}\n{extdb_output_script}\n{list_sample_output}")
        print(f"\n{GEOMOSAIC_NOTE}: These script can be considered minimal for SLURM.\nIf you need you can modify them to add more SBATCH information. More details can be retrieved to official SLURM Documentation.")
        print(f"\n{GEOMOSAIC_NOTE}: So now you are ready to go!\nYour first step should be to setup the required databases of your pipeline, by executing:\n{prompt1}\n\nonce it is finished, you can execute the real pipeline:\n{prompt2}")


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


def update_threads(unit, geomosaic_wdir, threads):
    filename = "config_unit.yaml" if unit else "config.yaml"
    config_file = os.path.join(geomosaic_wdir, filename)

    # CHECK CONFIG FILE EXISTS
    if not os.path.isfile(config_file):
        print(f"\n{GEOMOSAIC_ERROR}: '{filename}' does not exists in the Geomosaic WDIR: {geomosaic_wdir}")
        exit(1)
    
    # OPEN CONFIG FILE
    with open(config_file) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)

    # CHECK THREADS VALUE
    if threads != configs["threads"]:
        print(f"{GEOMOSAIC_PROCESS}: Geomosaic will overwite the 'threads' value in the config file since it is idifferent.")

        configs["threads"] = threads
        with open(config_file, 'w') as fd_config:
            yaml.dump(configs, fd_config)
