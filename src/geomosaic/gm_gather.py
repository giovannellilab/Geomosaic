import yaml
import os
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROCESS, GEOMOSAIC_OK, GEOMOSAIC_NOTE, GEOMOSAIC_PROMPT, GEOMOSAIC_GATHER_PACKAGES

from geomosaic.gathering.gather_eggnog_mapper import gather_eggnogmapper
from geomosaic.gathering.gather_hmms_search import gather_hmms_search
from geomosaic.gathering.gather_kaiju import gather_kaiju
from geomosaic.gathering.gather_kraken2 import gather_kraken2
from geomosaic.gathering.gather_mags_dram import gather_mags_dram
from geomosaic.gathering.gather_mags_gtdbtk import gather_mags_gtdbtk
from geomosaic.gathering.gather_mags_hmmsearch import gather_mags_hmmsearch
from geomosaic.gathering.gather_mags_recognizer import gather_mags_recognizer
from geomosaic.gathering.gather_mifaser import gather_mifaser
from geomosaic.gathering.gather_recognizer import gather_recognizer
from geomosaic.gathering.gather_coverm_genome import gather_coverm_genome


def geo_gather(args):
    gmsetup             = args.setup_file
    packages            = args.packages
    gather_folder       = args.gather_folder
    unit                = args.unit

    with open(gmsetup) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    geomosaic_dir       = geomosaic_setup["GEOMOSAIC_WDIR"]
    geomosaic_samples   = geomosaic_setup["SAMPLES"]

    name_config = "config_unit.yaml" if unit else "config.yaml"
    gm_config   = str(os.path.join(geomosaic_dir, name_config))

    output_gather_folder = create_gathering_folder(geomosaic_dir,gather_folder)

    user_packages = order_gathering(packages)
    
    if "coverm_genome" in user_packages and "mags_gtdbtk" not in user_packages:
        print(f"{GEOMOSAIC_ERROR}: The gathering for 'coverm_genome' need also to include 'mags_gtdbtk' in the gathering list.")
        exit(1)

    gathering = gather_functions()

    for pckg in user_packages:
        if pckg == "_ALL_":
            continue

        print(f"{GEOMOSAIC_PROCESS}: gathering results for {pckg}...")
        gathering[pckg](gm_config, geomosaic_dir, output_gather_folder)


def order_gathering(packages):
    if packages == ["_ALL_"]:
        user_packages = GEOMOSAIC_GATHER_PACKAGES

    else:
        user_packages = []
        failed_user_packages = []

        for i in GEOMOSAIC_GATHER_PACKAGES:
            user_packages.append(i) if i in packages else failed_user_packages.append(i)
    
    return user_packages


def gather_functions():
    return {
        "mifaser": gather_mifaser,
        "kaiju": gather_kaiju,

        "kraken2": gather_kraken2,
        "eggnog_mapper": gather_eggnogmapper,
        "recognizer": gather_recognizer,
        "hmms_search": gather_hmms_search,
        
        "mags_gtdbtk": gather_mags_gtdbtk,
        "mags_recognizer": gather_mags_recognizer,
        "mags_dram": gather_mags_dram,
        "mags_hmmsearch": gather_mags_hmmsearch,
        "coverm_genome": gather_coverm_genome
    }


def create_gathering_folder(geomosaic_dir,gather_folder):
    user_gather_folder = None
    if gather_folder is None:
        gather_folder = os.path.join(geomosaic_dir, "gm_gathering")
        if not os.path.isdir(gather_folder):
            user_gather_folder = gather_folder
            os.makedirs(user_gather_folder)
        else:
            user_gather_folder = gather_folder
    else:
        if not os.path.isdir(gather_folder):
            user_gather_folder = gather_folder
            os.makedirs(user_gather_folder)
        else:
            user_gather_folder = gather_folder
    
    return user_gather_folder
