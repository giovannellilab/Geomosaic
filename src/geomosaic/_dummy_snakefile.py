import yaml

def dummy_rule(package, condaenv):
    dummy_rule = """

rule dummy_{package}:
    output:
        file=temp("test_{package}.txt")
    conda:
        {condaenv}
    shell:
        """
    s = dummy_rule.format(package=package, condaenv=condaenv) +'"touch {output.file}"' + "\n\n"
    return s

def dummy_snakefile(config_env, configpath):
    dummy_snakefile = """
configfile: '{configpath}'

""".format(configpath=configpath)

    for pckg, _ in config_env.items():
        prefix = f'config["ENVS"]["{pckg}"]'
        dummy_snakefile += dummy_rule(pckg, prefix)

    return dummy_snakefile


def create_dummy_snakefile(config_file, configpath, filename_dummy_snakefile):
    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    s = dummy_snakefile(config["ENVS"], configpath)

    with open(filename_dummy_snakefile, "wt") as fd:
        fd.write(s)
