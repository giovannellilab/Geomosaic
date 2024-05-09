import json
import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_NOTE, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_MODULES, append_to_gmsetupyaml
from geomosaic._build_pipelines_module import import_graph, build_pipeline_modules, ask_additional_parameters
from geomosaic._compose import write_gmfiles, compose_config


def geo_unit(args):
    print(f"{GEOMOSAIC_PROCESS}: Loading variables from GeoMosaic setup file... ", end="", flush=True)
    gmsetup          = args.setup_file
    module              = args.module
    threads             = args.threads
    user_extdbfolder    = args.externaldb_gmfolder
    user_condafolder    = args.condaenv_gmfolder

    with open(gmsetup) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    samples_list                = geomosaic_setup["SAMPLES"]
    geomosaic_dir               = geomosaic_setup["GEOMOSAIC_WDIR"]

    geomosaic_user_parameters = os.path.join(geomosaic_dir, "gm_user_parameters")
    if not os.path.isdir(geomosaic_user_parameters):
        os.makedirs(geomosaic_user_parameters)

    geomosaic_condaenvs_folder = os.path.join(geomosaic_dir, "gm_conda_envs") if user_condafolder is None else user_condafolder
    if not os.path.isdir(geomosaic_condaenvs_folder):
        os.makedirs(geomosaic_condaenvs_folder)

    geomosaic_externaldb_folder = os.path.join(geomosaic_dir, "gm_external_db") if user_extdbfolder is None else user_extdbfolder
    if not os.path.isdir(geomosaic_externaldb_folder):
        os.makedirs(geomosaic_externaldb_folder)

    append_to_gmsetupyaml(gmsetup, {
        "GM_CONDA_ENVS": geomosaic_condaenvs_folder,
        "GM_USER_PARAMETERS": geomosaic_user_parameters,
        "GM_EXTERNAL_DB": geomosaic_externaldb_folder
    })
    
    print(GEOMOSAIC_OK)

    ## READ SETUPS FOLDERS AND FILE
    modules_folder          = os.path.join(os.path.dirname(__file__), 'modules')
    envs_folder             = os.path.join(os.path.dirname(__file__), 'envs')
    gmpackages_path         = os.path.join(os.path.dirname(__file__), 'gmpackages.json')
    gmpackages_extdb_path   = os.path.join(os.path.dirname(__file__), 'modules_extdb') 

    with open(gmpackages_path, 'rt') as f:
        gmpackages = json.load(f)

    G = import_graph(gmpackages["graph"])

    ## GMPACKAGES SECTIONS
    collected_modules   = gmpackages["modules"]
    order               = gmpackages["order"]
    additional_input    = gmpackages["additional_input"]
    envs                = gmpackages["envs"]
    gmpackages_extdb    = gmpackages["external_db"]

    ##############################
    ######### -- UNIT -- #########
    ##############################
    
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
    print("\nNow you need to specify the package/s that you used for those dependencies.")
    
    for dep in module_dependencies:
        temp_user_choices, _, _, _ = build_pipeline_modules(
            graph               = G,
            collected_modules   = collected_modules, 
            order               = order, 
            additional_input    = additional_input,
            mstart              = dep,
            unit                = True,
            dependencies        = True
        )
        raw_user_choices[dep] = temp_user_choices[dep]
    
    user_choices = {}
    for m in order:
        if m in raw_user_choices:
            user_choices[m] = raw_user_choices[m]

    ## ASK ADDITIONAL PARAMETERS
    additional_parameters = ask_additional_parameters(additional_input, order_writing)
    
    config_filename     = os.path.join(geomosaic_dir, "config_unit.yaml")
    snakefile_filename  = os.path.join(geomosaic_dir, "Snakefile_unit.smk")
    snakefile_extdb     = os.path.join(geomosaic_dir, "Snakefile_extdb.smk")

    ## CONFIG FILE SETUP
    config = compose_config(geomosaic_dir, samples_list, additional_parameters, 
                            user_choices, modules_folder, 
                            geomosaic_user_parameters, 
                            envs, envs_folder, geomosaic_condaenvs_folder,
                            geomosaic_externaldb_folder, gmpackages_extdb, threads)

    ## SNAKEFILE FILE SETUP
    write_gmfiles(config_filename, config, 
                  snakefile_filename, snakefile_extdb, 
                  user_choices, order_writing, 
                  modules_folder, 
                  gmpackages_extdb, gmpackages_extdb_path)
    
    # # Draw DAG
    # dag_image = os.path.join(geomosaic_dir, "dag.pdf")
    # subprocess.check_call(f"snakemake -s {snakefile_filename} --rulegraph | dot -Tpdf > {dag_image}", shell=True)
