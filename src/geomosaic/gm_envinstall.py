import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK
from subprocess import check_call


def geo_envinstall(args):
    print(f"{GEOMOSAIC_PROCESS}: Installing all the conda environments of your workflow/unit. This may take a while...\n\n", end="", flush=True)
    setup_file  = args.setup_file
    unit        = args.unit

    with open(setup_file) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    geomosaic_dir = geomosaic_setup["GEOMOSAIC_WDIR"]

    name_snakefile = "Snakefile_unit.smk" if unit else "Snakefile.smk"
    gm_snakefile = str(os.path.join(geomosaic_dir, name_snakefile))

    check_call(["snakemake", "--use-conda", "--conda-create-envs-only", "--cores", "1", "-s", gm_snakefile])
    
    print(GEOMOSAIC_OK)
