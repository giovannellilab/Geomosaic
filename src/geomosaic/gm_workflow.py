import json
import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_NOTE
from geomosaic._build_pipelines_module import import_graph, build_pipeline_modules, ask_additional_parameters
from geomosaic._compose import write_gmfiles, compose_config


def geo_workflow(args):
    print(f"{GEOMOSAIC_PROCESS}: Loading variables from GeoMosaic setup file... ", end="", flush=True)
    setup_file          = args.setup_file
    glab                = args.glab
    mstart              = args.module_start
    threads             = args.threads
    user_extdbfolder    = args.externaldb_gmfolder

    with open(setup_file) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    samples_list    = geomosaic_setup["SAMPLES"]
    geomosaic_dir   = geomosaic_setup["GEOMOSAIC_WDIR"]

    geomosaic_user_parameters   = os.path.join(geomosaic_dir, "gm_user_parameters")
    if not os.path.isdir(geomosaic_user_parameters):
        os.makedirs(geomosaic_user_parameters)

    geomosaic_condaenvs_folder   = os.path.join(geomosaic_dir, "gm_conda_envs")
    if not os.path.isdir(geomosaic_condaenvs_folder):
        os.makedirs(geomosaic_condaenvs_folder)
    
    if user_extdbfolder is None:
        geomosaic_externaldb_folder   = os.path.join(geomosaic_dir, "gm_external_db")
        if not os.path.isdir(geomosaic_externaldb_folder):
            os.makedirs(geomosaic_externaldb_folder)
    else:
        geomosaic_externaldb_folder = user_extdbfolder

    print(GEOMOSAIC_OK)

    ## READ SETUPS FOLDERS AND FILE
    modules_folder          = os.path.join(os.path.dirname(__file__), 'modules')
    gmpackages_path         = os.path.join(os.path.dirname(__file__), 'gmpackages.json')
    envs_folder             = os.path.join(os.path.dirname(__file__), 'envs')
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

    ##################################
    ######### -- WORKFLOW -- #########
    ##################################

    if glab:
        # TODO: Adding additional parameters to default pipeline
        with open(os.path.join(os.path.dirname(__file__), 'pipeline.json')) as default_pipeline:
            pipe                    = json.load(default_pipeline)
            user_choices            = pipe["user_choices"]
            order_writing           = pipe["order_writing"]
            additional_parameters   = pipe["additional_parameters"]
    else:
        # NOTE: BUILDING PIPELINE BASED ON USER CHOICES
        if mstart != "pre_processing":
            user_choices, dependencies, \
                modified_G, order_writing = middle_start(mstart, G, collected_modules, order, additional_input)
        else:    
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


def middle_start(mstart, G, collected_modules, order, additional_input):
    raw_user_choices, dependencies, modified_G, order_writing = build_pipeline_modules(
        graph               = G,
        collected_modules   = collected_modules, 
        order               = order, 
        additional_input    = additional_input,
        mstart              = mstart,
        unit                = False
    )

    module_dependencies = list(G.predecessors(mstart))
    print(f"{GEOMOSAIC_NOTE}: You've chosen to start the workflow from a different node. It is assumed also that those modules dependencies have already been run with GeoMosaic")
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

    return user_choices, dependencies, modified_G, order_writing
