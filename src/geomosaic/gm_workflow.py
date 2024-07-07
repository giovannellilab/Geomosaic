import json
import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_NOTE, append_to_gmsetupyaml
from geomosaic._build_pipelines_module import import_graph, build_pipeline_modules, ask_additional_parameters
from geomosaic._compose import write_gmfiles, compose_config
from geomosaic._draw import geomosaic_draw_workflow


def geo_workflow(args):
    print(f"{GEOMOSAIC_PROCESS}: Loading variables from GeoMosaic setup file... ", end="", flush=True)
    gmsetup             = args.setup_file
    pipeline            = args.pipeline
    mstart              = args.module_start
    threads             = args.threads

    with open(gmsetup) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    
    assert "GM_CONDA_ENVS" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: Conda Env directory must be provided with the key 'GM_CONDA_ENVS'"
    assert "GM_USER_PARAMETERS" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: User parameters directory must be provided with the key 'GM_USER_PARAMETERS'"
    assert "GM_EXTERNAL_DB" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: External DB directory must be provided with the key 'GM_EXTERNAL_DB'"
    
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    samples_list                = geomosaic_setup["SAMPLES"]
    geomosaic_dir               = geomosaic_setup["GEOMOSAIC_WDIR"]
    geomosaic_condaenvs_folder  = geomosaic_setup["GM_CONDA_ENVS"]
    geomosaic_user_parameters   = geomosaic_setup["GM_USER_PARAMETERS"]
    geomosaic_externaldb_folder = geomosaic_setup["GM_EXTERNAL_DB"]

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

    if pipeline == "glab":
        # TODO: Adding additional parameters to default pipeline
        with open(os.path.join(os.path.dirname(__file__), 'glab.json')) as default_pipeline:
            pipe                    = json.load(default_pipeline)
            user_choices            = pipe["user_choices"]
            order_writing           = pipe["order_writing"]
            additional_parameters   = pipe["additional_parameters"]
            skipped_modules         = pipe["skipped_modules"]
    elif pipeline == "just_mags":
        with open(os.path.join(os.path.dirname(__file__), 'just_mags.json')) as default_pipeline:
            pipe                    = json.load(default_pipeline)
            user_choices            = pipe["user_choices"]
            order_writing           = pipe["order_writing"]
            additional_parameters   = pipe["additional_parameters"]
            skipped_modules         = pipe["skipped_modules"]
    else:
        # NOTE: BUILDING PIPELINE BASED ON USER CHOICES
        if mstart != "pre_processing":
            user_choices, dependencies, \
                modified_G, order_writing, skipped_modules = middle_start(mstart, G, collected_modules, order, additional_input)
        else:    
            user_choices, dependencies, modified_G, order_writing, skipped_modules = build_pipeline_modules(
                graph               = G,
                collected_modules   = collected_modules, 
                order               = order, 
                additional_input    = additional_input,
                mstart              = mstart
            )

        ## ASK ADDITIONAL PARAMETERS
        additional_parameters = ask_additional_parameters(additional_input, order_writing)
    
    # print("=======USER_CHOICES=======")
    # print(user_choices)
    # print("=======ADDITIONAL_PARAMETERS=======")
    # print(additional_parameters)
    # print("=======ORDER_WRITING=======")
    # print(order_writing)
    # print("=======SKIPPED_MODULES=======")
    # print(skipped_modules)

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
    
    print(f"{GEOMOSAIC_NOTE}: drawing your workflow graph...")
    geomosaic_draw_workflow(gmpackages_path, user_choices, skipped_modules)

def middle_start(mstart, G, collected_modules, order, additional_input):
    raw_user_choices, dependencies, modified_G, order_writing, skipped_modules = build_pipeline_modules(
        graph               = G,
        collected_modules   = collected_modules, 
        order               = order, 
        additional_input    = additional_input,
        mstart              = mstart,
        unit                = False
    )

    module_dependencies = retrieve_all_dependencies(G, mstart, raw_user_choices, order)
    
    print(f"{GEOMOSAIC_NOTE}: You've chosen to start the workflow from a different node. It is assumed also the modules dependencies have already been run with GeoMosaic")
    print(f"{GEOMOSAIC_NOTE}: '{mstart}' depends on the following modules:\n"+"\n".join(map(lambda x: f"\t- {x}", module_dependencies)))
    print("\nNow you need to specify the package/s that you used for those dependencies.")
    
    for dep in module_dependencies:
        temp_user_choices, _, _, _, _ = build_pipeline_modules(
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

    return user_choices, dependencies, modified_G, order_writing, skipped_modules


def retrieve_all_dependencies(G, mstart, user_choices, order):
    module_dependencies = set(G.predecessors(mstart))

    for m, _ in user_choices.items():
        preds = list(G.predecessors(m))
        for x in preds:
            if x not in user_choices:
                module_dependencies.add(x)
    
    sorted_md = [o for o in order if o in module_dependencies]

    return sorted_md
