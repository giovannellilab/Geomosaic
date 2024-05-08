import yaml


def dummy_rule(geomosaic_wdir, package, condaenv):
    outfilename = "{wdir}/geomosaic_temp_{package}.txt".format(wdir=geomosaic_wdir, package=package)

    dr = """

rule dummy_{package}:
    output:
        file=temp("{outfilename}")
    conda:
        {condaenv}
    shell:
        """
    s = dr.format(outfilename=outfilename, condaenv=condaenv, package=package) +'"touch {output.file}"' + "\n\n"
    return s, outfilename


def make_inputs_allrule(list_outfilenames):
    s = ""
    for f in list_outfilenames:
        if f == list_outfilenames[-1]:
            s += f"\t\t{f}\n"
        else:
            s += f"\t\t{f},\n\n\n"
    
    return s


def dummy_snakefile(geomosaic_wdir, config_env, configpath):
    all_rules = ""
    all_outfilenames = []

    for pckg, _ in config_env.items():
        prefix = f'config["ENVS"]["{pckg}"]'
        dr, of = dummy_rule(geomosaic_wdir, pckg, prefix)
        all_rules += dr
        all_outfilenames.append(of)

    dummy_snakefile = """
configfile: '{configpath}'

rule all:
    input:
""".format(configpath=configpath) + make_inputs_allrule(all_outfilenames) + all_rules
    
    return dummy_snakefile


def create_dummy_snakefile(geomosaic_wdir, config_file_path, filename_dummy_snakefile):
    with open(config_file_path) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    s = dummy_snakefile(geomosaic_wdir, config["ENVS"], config_file_path)

    with open(filename_dummy_snakefile, "wt") as fd:
        fd.write(s)
