import yaml
import os
import shutil
from geomosaic._utils import GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_NOTE


def compose_config(geomosaic_dir, samples_list, additional_parameters, user_choices, \
                   modules_folder, geomosaic_user_parameters, envs, envs_folder, geomosaic_condaenvs_folder, \
                    geomosaic_externaldb_folder, gmpackages_extdb, \
                        threads):
    ## CONFIG FILE SETUP
    config = {}

    config["SAMPLES"]   = samples_list
    config["WDIR"]      = os.path.abspath(geomosaic_dir)
    config["threads"]   = threads

    config["ADDITIONAL_PARAM"] = {}
    for ap, ap_input in additional_parameters.items():
        config["ADDITIONAL_PARAM"][ap] = ap_input

    config["MODULES"]   = {}
    for module_name, pckg in user_choices.items():
        config["MODULES"][module_name] = pckg

    ## COPY USER PARAMS on the CORRESPONDING LOCATION and SAVE ENVS location
    for um, up in user_choices.items():

        ## USER PARAMS -- SECTION
        if "USER_PARAMS" not in config:
            config["USER_PARAMS"] = {}
        
        up_src_param = os.path.join(modules_folder, um, up, "param.yaml")
        up_dst_param = os.path.join(geomosaic_user_parameters, f"{up}.yaml")
        if not os.path.isfile(up_dst_param):
            shutil.copyfile(up_src_param, up_dst_param)
        
        config["USER_PARAMS"][up] = up_dst_param

        ## ENVS -- SECTION
        if "ENVS" not in config:
            config["ENVS"] = {}
        
        if "ENVS_EXTDB" not in config:
            config["ENVS_EXTDB"] = {}

        if up in envs:
            up_src_envs = os.path.join(envs_folder, envs[up])
            up_dst_envs = os.path.join(geomosaic_condaenvs_folder, f"{up}_env.yaml")
            
            shutil.copyfile(up_src_envs, up_dst_envs)
            
            config["ENVS"][up] = up_dst_envs

            ## ENV for EXTDB - TODO: OPTIMIZE this section
            if up in gmpackages_extdb:
                config["ENVS_EXTDB"][gmpackages_extdb[up]["inpfolder"]] = up_dst_envs

        ## EXTDB -- SECTION
        if "EXT_DB" not in config:
            config["EXT_DB"] = {}
        
        if up in gmpackages_extdb:
            config["EXT_DB"][gmpackages_extdb[up]["inpfolder"]] = str(os.path.join(geomosaic_externaldb_folder, gmpackages_extdb[up]["outfolder"]))

    return config


def write_gmfiles(config_filename, config, snakefile_filename, snakefile_extdb, user_choices, order_writing, modules_folder, gmpackages_extdb, gmpackages_extdb_path):
    # WRITING CONFIG FILE
    with open(config_filename, 'w') as fd_config:
        yaml.dump(config, fd_config)

    ## WRITING SNAKEFILE
    with open(snakefile_filename, "wt") as fd:
        fd.write(f"import yaml\n\n")
        fd.write(f"configfile: {str(repr(os.path.abspath(config_filename)))}\n")

        # Rule all
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

    write_extdb_snakefile(snakefile_extdb, config_filename, order_writing, user_choices, gmpackages_extdb, gmpackages_extdb_path)


def write_extdb_snakefile(snakefile_extdb, config_filename, order_writing, user_choices, gmpackages_extdb, gmpackages_extdb_path):
    # Rule for external DB
    external_added = set()
    for e in order_writing:
        tool = user_choices[e]
        if tool in gmpackages_extdb and gmpackages_extdb[tool]["inpfolder"] not in external_added:
            extdb_snakefile = gmpackages_extdb[tool]["inpfolder"]
            external_added.add(extdb_snakefile)

    if len(external_added) > 0:
        print(f"{GEOMOSAIC_PROCESS}: Building preliminary workflow to prepare all the database of your workflow...", end="", flush=True)
        ## WRITING SNAKEFILE EXTDB
        with open(snakefile_extdb, "wt") as fd:
            fd.write(f"import yaml\n\n")
            fd.write(f"configfile: {str(repr(os.path.abspath(config_filename)))}\n")

            fd.write("\nrule all:\n\tinput:\n\t\t")
            for t in external_added:
                t_extdb_snakefile = os.path.join(gmpackages_extdb_path, t, "target.txt")
                with open(t_extdb_snakefile) as sf:
                    fd.write(sf.read())
                    fd.write("\n\t\t")


            for t in external_added:
                t_extdb_snakefile = os.path.join(gmpackages_extdb_path, t, "snakefile.smk")
                with open(t_extdb_snakefile) as sf:
                    fd.write(sf.read())
        print(GEOMOSAIC_OK)
    else:
        print(f"{GEOMOSAIC_NOTE}: your workflow doesn't need the preparation of external database.")
        print(GEOMOSAIC_OK)
