import yaml
import os
import shutil


def compose_config(geomosaic_dir, samples_list, additional_parameters, user_choices, \
                   modules_folder, geomosaic_user_parameters, envs, envs_folder, geomosaic_externaldb_folder, gmpackages_extdb):
    ## CONFIG FILE SETUP
    config = {}

    config["SAMPLES"]   = samples_list
    config["WDIR"]      = os.path.abspath(geomosaic_dir)

    for ap, ap_input in additional_parameters.items():
        config[ap] = ap_input

    for module_name, pckg in user_choices.items():
        config[module_name] = pckg

    ## COPY USER PARAMS on the CORRESPONDING LOCATION and SAVE ENVS location
    for um, up in user_choices.items():
        up_src_param = os.path.join(modules_folder, um, up, "param.yaml")
        up_dst_param = os.path.join(geomosaic_user_parameters, f"{up}.yaml")

        if not os.path.isfile(up_dst_param):
            shutil.copyfile(up_src_param, up_dst_param)

        if "EXT_DB" not in config:
            config["EXT_DB"] = {}
        
        if up in gmpackages_extdb:
            config["EXT_DB"][up] = str(os.path.join(geomosaic_externaldb_folder, gmpackages_extdb[up]["outfolder"]))

        if "USER_PARAMS" not in config:
            config["USER_PARAMS"] = {}

        if "ENVS" not in config:
            config["ENVS"] = {}

        config["USER_PARAMS"][up] = up_dst_param

        if up in envs:
            up_env_location = os.path.join(envs_folder, envs[up])
            config["ENVS"][up] = up_env_location

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
