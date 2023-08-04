import json
import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_NOTE
from geomosaic._build_pipelines_module import import_graph, check_user_input, ask_additional_parameters
import subprocess


def geo_unit(args):
    config_file = args.config_file
    module      = args.module

    with open(config_file) as file:
        geomosaic_config_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_config_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_config_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"

    samples_list    = geomosaic_config_setup["SAMPLES"]
    geomosaic_dir   = geomosaic_config_setup["GEOMOSAIC_WDIR"]

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

    assert module in collected_modules, f"\n{GEOMOSAIC_ERROR}: chosen module does not exists. Please choose of the the following" + "\n".join(collected_modules)
    
    mstart = module
    module_dependencies = list(G.predecessors(mstart))
    print(f"{GEOMOSAIC_NOTE}: '{mstart}' depends on the following modules:\n"+"\n".join(map(lambda x: f"\t- {x}", module_dependencies)))
    print("\nIt is assumed also that those modules dependencies have already been run with GeoMosaic")

    user_choices = {}
    order_writing = module_dependencies + [mstart]
    for dep in order_writing:
        status = False
        module_descr = collected_modules[dep]["description"]
        module_choices = {}
        for indice, raw_package in enumerate(collected_modules[dep]["choices"].items(), start=1):
            pckg_display, pckg_name = raw_package
            module_choices[indice] = {"display": pckg_display, "package": pckg_name}

        prompt_display = f"\n{module_descr}\n" + "\n".join([f"{integer}) {pck_info['display']}" for integer, pck_info in module_choices.items()])
        while not status:
            print(prompt_display)
            
            raw_input = input()

            status, obj = check_user_input(raw_input, list(module_choices.keys()))
            if not status:
                print(obj)
        
        parse_input = obj
        
        user_choices[dep] = module_choices[parse_input]["package"]
    
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
