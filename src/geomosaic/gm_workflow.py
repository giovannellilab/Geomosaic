import json
import yaml
import os
import subprocess
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK
from geomosaic._build_pipelines_module import import_graph, build_pipeline_modules, ask_additional_parameters
from geomosaic.gm_compose import write_gmfiles, compose_config
import time


def geo_workflow(args):
    print(f"{GEOMOSAIC_PROCESS}: Loading variables from GeoMosaic setup file... ", end="", flush=True)
    setup_file  = args.setup_file
    pipeline    = args.pipeline
    mstart      = args.module_start

    with open(setup_file) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    samples_list    = geomosaic_setup["SAMPLES"]
    geomosaic_dir   = geomosaic_setup["GEOMOSAIC_WDIR"]

    geomosaic_user_parameters   = os.path.join(geomosaic_dir, "module_user_parameters")
    if not os.path.isdir(geomosaic_user_parameters):
        os.makedirs(geomosaic_user_parameters)

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

    if pipeline:
        # TODO: Adding additional parameters to default pipeline
        with open(os.path.join(os.path.dirname(__file__), 'pipeline.json')) as default_pipeline:
            pipe                    = json.load(default_pipeline)
            user_choices            = pipe["user_choices"]
            order_writing           = pipe["order_writing"]
            additional_parameters   = pipe["additional_parameters"]
    else:
        # NOTE: BUILDING PIPELINE BASED ON USER CHOICES
        user_choices, dependencies, modified_G, order_writing = build_pipeline_modules(
            graph               = G,
            collected_modules   = collected_modules, 
            order               = order, 
            additional_input    = additional_input,
            mstart              = mstart
        )
        ## ASK ADDITIONAL PARAMETERS
        additional_parameters = ask_additional_parameters(additional_input, order_writing)
    
    config_filename     = os.path.join(geomosaic_dir, "config.yaml")
    snakefile_filename  = os.path.join(geomosaic_dir, "Snakefile.smk")

    ## CONFIG FILE SETUP
    config = compose_config(geomosaic_dir, samples_list, additional_parameters, 
                            user_choices, modules_folder, geomosaic_user_parameters, envs, envs_folder)

    ## SNAKEFILE FILE SETUP
    write_gmfiles(config_filename, config, snakefile_filename, user_choices, order_writing, modules_folder)
    
    # Draw DAG
    dag_image = os.path.join(geomosaic_dir, "dag.pdf")
    subprocess.check_call(f"snakemake -s {snakefile_filename} --rulegraph | dot -Tpdf > {dag_image}", shell=True)

