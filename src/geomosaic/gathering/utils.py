import yaml
from geomosaic._utils import GEOMOSAIC_ERROR
import os
from subprocess import check_call


def essential_data_config(gmsetup, path_gathering):
    with open(gmsetup) as file:
        geomosaic_setup = yaml.load(file, Loader=yaml.FullLoader)

    assert "SAMPLES" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: sample list must be provided with the key 'SAMPLES'"
    assert "GEOMOSAIC_WDIR" in geomosaic_setup, f"\n{GEOMOSAIC_ERROR}: geomosaic working directory must be provided with the key 'GEOMOSAIC_WDIR'"
    assert os.path.isdir(geomosaic_setup["GEOMOSAIC_WDIR"]), f"\n{GEOMOSAIC_ERROR}: GeoMosaic working directory does not exists."

    geomosaic_dir = geomosaic_setup["GEOMOSAIC_WDIR"]
    geomosaic_samples = geomosaic_setup["SAMPLES"]

    geomosaic_gathering = os.path.join(geomosaic_dir, "gm_gathering") if path_gathering is None else path_gathering
    
    if not os.path.isdir(geomosaic_gathering):
        os.makedirs(geomosaic_gathering)
    
    return geomosaic_samples, geomosaic_gathering


def get_sample_with_results(result_folder, geomosaic_wdir, all_samples):
    true_samples = []
    for s in all_samples:
        if result_folder in os.listdir(os.path.join(geomosaic_wdir, s)): 
            true_samples.append(s)
    
    return true_samples
