import json
import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_NOTE, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_MODULES
from geomosaic._build_pipelines_module import import_graph, build_pipeline_modules, ask_additional_parameters
import subprocess
import time


def geo_unit(args):
    print(f"{GEOMOSAIC_PROCESS}: Loading variables from GeoMosaic setup file... ", end="", flush=True)
    setup_file  = args.setup_file
    module      = args.module

    with open(setup_file) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    samples_list    = geomosaic_setup["SAMPLES"]
    geomosaic_dir   = geomosaic_setup["GEOMOSAIC_WDIR"]
    time.sleep(1)
    print(GEOMOSAIC_OK)

    ## READ SETUPS FOLDERS AND FILE
    modules_folder  = os.path.join(os.path.dirname(__file__), 'modules')
    gmpackages_path = os.path.join(os.path.dirname(__file__), 'gmpackages.json')
    envs_folder     = os.path.join(os.path.dirname(__file__), 'envs')

    with open(gmpackages_path, 'rt') as f:
        gmpackages = json.load(f)

    G = import_graph(gmpackages["graph"])

    ## GMPACKAGES SECTIONS
    collected_modules   = gmpackages["modules"]
    order               = gmpackages["order"]
    additional_input    = gmpackages["additional_input"]
    envs                = gmpackages["envs"]

    assert module in collected_modules, f"\n\n{GEOMOSAIC_ERROR}: chosen module does not exists. Please choose of the the following\n {GEOMOSAIC_MODULES}"
    
    mstart = module
    order_writing = [mstart]
    raw_user_choices, _, _, _ = build_pipeline_modules(
        graph               = G,
        collected_modules   = collected_modules, 
        order               = order, 
        additional_input    = additional_input,
        mstart              = mstart,
        unit                = True
    )

    module_dependencies = list(G.predecessors(mstart))
    print(f"{GEOMOSAIC_NOTE}: It is assumed also that those modules dependencies have already been run with GeoMosaic")
    print(f"{GEOMOSAIC_NOTE}: '{mstart}' depends on the following modules:\n"+"\n".join(map(lambda x: f"\t- {x}", module_dependencies)))
    print("You need to specify the package/s that you used for those dependencis.")
    
    for dep in module_dependencies:
        temp_user_choices, _, _, _ = build_pipeline_modules(
            graph               = G,
            collected_modules   = collected_modules, 
            order               = order, 
            additional_input    = additional_input,
            mstart              = dep,
            unit                = True
        )
        raw_user_choices[dep] = temp_user_choices[dep]
    
    user_choices = {}
    for m in order:
        if m in raw_user_choices:
            user_choices[m] = raw_user_choices[m]
    
    chosen_packages = user_choices.values()

    ## ASK ADDITIONAL PARAMETERS
    additional_parameters = ask_additional_parameters(additional_input, order_writing)
    
    config_filename     = os.path.join(geomosaic_dir, "config_unit.yaml")
    snakefile_filename  = os.path.join(geomosaic_dir, "Snakefile_unit.smk")

    ## CONFIG FILE SETUP
    config = {}

    config["SAMPLES"]   = samples_list
    config["WDIR"]      = os.path.abspath(geomosaic_dir)    

    for ap, ap_input in additional_parameters.items():
        config[ap] = ap_input

    for module_name, pckg in user_choices.items():
        config[module_name] = pckg

    for env_pkg, env_file in envs.items():
        if env_pkg in chosen_packages:
            if "ENVS" not in config:
                config["ENVS"] = {}

            config["ENVS"][env_pkg] = os.path.join(envs_folder, env_file)

    # WRITING CONFIG FILE
    with open(config_filename, 'w') as fd_config:
        yaml.dump(config, fd_config)

    ## WRITING SNAKEFILE
    with open(snakefile_filename, "wt") as fd:
        fd.write(f"configfile: {str(repr(os.path.abspath(config_filename)))}\n")

        # Rule ALL
        fd.write("\nrule all:\n\tinput:\n\t\t")
        for m in order_writing:
            package = user_choices[m]
            snakefile_target = os.path.join(modules_folder, m, package, "Snakefile_target.smk")

            with open(snakefile_target) as file:
                target = yaml.load(file, Loader=yaml.FullLoader)
            
            input_target = target[f"rule all_{package}"]["input"]
            fd.write(f"{input_target}\n\t\t")
                    
        # Rule for each package
        for i in order_writing:
            pckg_chosen = user_choices[i]
            with open(os.path.join(modules_folder, i, pckg_chosen, "Snakefile.smk")) as sf:
                fd.write(sf.read())
    
    # Draw DAG
    dag_image = os.path.join(geomosaic_dir, "dag.pdf")
    subprocess.check_call(f"snakemake -s {snakefile_filename} --rulegraph | dot -Tpdf > {dag_image}", shell=True)
