import yaml


def dummy_rule(geomosaic_wdir, package, condaenv):
    outfilename = "{wdir}/geomosaic_temp_{package}.txt".format(wdir=geomosaic_wdir, package=package)

    dummy_rule = """

rule dummy_{package}:
    output:
        file=temp("{outfilename}")
    conda:
        {condaenv}
    shell:
        """
    s = dummy_rule.format(outfilename=outfilename, condaenv=condaenv) +'"touch {output.file}"' + "\n\n"
    return s, outfilename


def make_inputs_allrule(list_outfilenames):
    s = ""
    for f in list_outfilenames:
        if f == list_outfilenames[-1]:
            s += f"\t\t{f}\n"
        else:
            s += f"\t\t{f},\n\n\n"
    
    return s


def dummy_snakefile(config_env, configpath):
    all_rules = ""
    all_outfilenames = []

    for pckg, _ in config_env.items():
        prefix = f'config["ENVS"]["{pckg}"]'
        dr, of = dummy_rule(pckg, prefix)
        all_rules += dr
        all_outfilenames.append(of)

    dummy_snakefile = """
configfile: '{configpath}'

rule all:
    input:
""".format(configpath=configpath) + make_inputs_allrule(all_outfilenames) + all_rules
    
    return dummy_snakefile


def create_dummy_snakefile(config_file, configpath, filename_dummy_snakefile):
    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    s = dummy_snakefile(config["ENVS"], configpath)

    with open(filename_dummy_snakefile, "wt") as fd:
        fd.write(s)
