import os
import re
import pandas as pd
import numpy as np
from itertools import product
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROMPT, GEOMOSAIC_OK, GEOMOSAIC_NOTE
from geomosaic._validator import check_special_characters_on_string


def _prepare_metalindex_customdb_generic(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder, folder_name: str):
    # USER FILES
    config_customdb_section["user_metal_table"] = collected_info["redox_metal_index_file_table"]
    config_customdb_section["output_folder"] = folder_name

    basename_table = os.path.basename(collected_info["redox_metal_index_file_table"])

    # EXTDB Section
    config_extdb_section["database_folder"] = os.path.join(geomosaic_externaldb_folder, folder_name)
    config_extdb_section["table_file"] = os.path.join(geomosaic_externaldb_folder, folder_name, basename_table)


def prepare_metalindex_customdb(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder):
    _prepare_metalindex_customdb_generic(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder, "redox_metal_plasticity_index")


def prepare_metalindex_customdb_kofam(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder):
    _prepare_metalindex_customdb_generic(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder, "kofam_scan_redox_metal_plasticity_index")


def prepare_metalindex_customdb_mags_kofam(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder):
    _prepare_metalindex_customdb_generic(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder, "mags_kofam_scan_redox_metal_plasticity_index")

def check_file(file_path: str):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.tsv':
        return pd.read_csv(file_path, sep='\t'), ext
    elif ext == '.csv':
        return pd.read_csv(file_path, sep=','), ext
    elif ext in ['.xlsx', '.xls']:
        return pd.read_excel(file_path), ext
    else:
        return pd.read_csv(file_path, sep='\t'), ext


def validator_metal_index_file(file_path:str):

    na1 = ',["@!#$%^&*()<>?/\|}{~:;]'
    na2 = "'`€¹²³¼½¬="

    regex1 = re.compile(na1)
    regex2 = re.compile(na2)

    if " " in file_path:
        print(f"{GEOMOSAIC_ERROR}: the provided file {str(repr(file_path))} does contain a space. To avoid later issues, please rename the file without any space.")
        return False
    
    if(regex1.search(file_path) != None):
        print(f"{GEOMOSAIC_ERROR}: the provided file does contain a special character that is not allowed: {str(repr(file_path))}\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False

    if(regex2.search(file_path) != None):
        print(f"{GEOMOSAIC_ERROR}: the provided file does contain a special character that is not allowed: {str(repr(file_path))}\n\
          The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False

    if not os.path.exists(file_path):
        print(f"{GEOMOSAIC_ERROR}: the provided file does not exist.")
        return False


    df, extension = check_file(file_path)

    required_cols = ["energyRole", "biogeoSubstrate", "Metal", "KO"]
    missing = [col for col in required_cols if col not in df.columns]
     
    if missing:
        print(f"{GEOMOSAIC_ERROR}: the provided {extension} table {str(repr(file_path))} does not contain minimal the required columns {required_cols}")
        return False
    

    na3 = '^K\d{5}$'
    na4 = '^[AD](\s*,\s*[AD])*$'

    invalid_kos = df[~df['KO'].astype(str).str.match(na3)]

    if invalid_kos.KO.nunique() > 0:
        print(f"{GEOMOSAIC_ERROR}: the provided {extension} table {str(repr(file_path))} does not contain the required columns \n\
              Please, provide minimal requested columns: {invalid_kos}")
        return False


    invalid_enrgyrole = df[~df['energyRole'].astype(str).str.match(na4)]

    if invalid_enrgyrole.energyRole.nunique() > 0:
        print(f"{GEOMOSAIC_ERROR}: the provided {extension} table {str(repr(file_path))} does not contain the required columns \n\
              Please, provide minimal requested columns: {invalid_enrgyrole}")
        return False

    return True


def redox_metabolic_index(acceptors_list: list, donors_list: list) -> float:
    """
    Computes the Redox-Metabolic Index (RMI) as:
    RMI = log(len(unique donors)) + log(len(unique acceptors))
    """
    if len(donors_list) == 0 or len(acceptors_list) == 0:
        return 0.0

    return float(round(np.log(len(donors_list)) + np.log(len(acceptors_list)), 4))


def metal_plasticity_index(metal_donors_l: list, metal_acceptor_l: list) -> float:
    """
    Computes the Redox-Plasticity Index (RPI/MPI) as:
    RPI = log(len(unique metal pairs))
    """
    if len(metal_donors_l) == 0 or len(metal_acceptor_l) == 0:
        return 0.0

    unique_pairs = list({tuple(sorted(pair)) for pair in product(metal_donors_l, metal_acceptor_l)})

    return float(round(np.log(len(unique_pairs)), 4))


def substrate_metal_map(df: pd.DataFrame) -> tuple[dict[str, dict], list[str], list[str]]:
    """
    Builds a substrate -> {metal -> [KOs]} map from a biogeochemical table
    already filtered by energyRole (donors or acceptors).
    """
    substrate_map = {}
    unique_metals, unique_substrates = set(), set()
    no_metal = "__no_metal__"

    for _, row in df.iterrows():

        substrate = row['biogeoSubstrate']
        metal = row['Metal']
        ko = row['KO']
        unique_substrates.add(substrate)

        if substrate not in substrate_map:
            substrate_map[substrate] = {"metals": {}}

        if isinstance(metal, str) and metal != '//':
            metals = [m.strip() for m in metal.split(',')]
            for m in metals:
                unique_metals.add(m)
                if m not in substrate_map[substrate]["metals"]:
                    substrate_map[substrate]["metals"][m] = [ko]
                else:
                    substrate_map[substrate]["metals"][m].append(ko)

        elif metal == '//':
            if no_metal not in substrate_map[substrate]["metals"]:
                substrate_map[substrate]["metals"][no_metal] = [ko]
            else:
                substrate_map[substrate]["metals"][no_metal].append(ko)

    return substrate_map, sorted(list(unique_metals)), sorted(list(unique_substrates))


def parse_results(s, d: dict, index_substrate_pairs: float, index_metal_pairs: float, type_s: str) -> pd.DataFrame:
    """
    Flattens the substrate_metal_map output into a long-format DataFrame,
    one row per (substrate, metal) pair, tagged with the sample, computed
    indexes, and donor/acceptor type.
    """
    rows = []
    for substrate, data in d.items():
        for metal, kos in data["metals"].items():
            rows.append({'sample': s, 'rmi': index_substrate_pairs, 'mpi': index_metal_pairs,
                         'substrate': substrate, 'metal': np.nan if metal == "__no_metal__" else metal,
                         'type': type_s, "KO": kos})
    return pd.DataFrame(rows)


metal_index_database_structure = GEOMOSAIC_PROMPT("""
#####################################
##### REDOX METAL PLASTICTY INDEX CUSTOM MODULE ##### 
#####################################
This module allows you to provide a custom table with metal indexes information.
The table must be in .tsv, .csv or .xlsx format and MUST contain the following columns:
energyRole, biogeoSubstrate, Metal, KO.
                                                  
- The energyRole column must contain the energy role of the metal index (e.g., A for acceptor, D for donor).
- The biogeoSubstrate refers to the Acceptor/Donor substrate contain the biogeochemical substrate associated with the metal index (e.g., Fe, Mn, S). \n\
- The Metal column must contain the name of the metal associated with the index (e.g., Iron = Fe, Nickel = Ni, ).
- The KO column must contain the KEGG Orthology (KO) identifier associated with the metal index (e.g., K00001).

An example of a minimal Redox-metabolic & Plasticity table structure is provided below:

| energyRole | biogeoSubstrate  | Metal  | KO      |
|------------|----------------- |--------|---------|
| A          |  CO2             | Fe     | K00197  |
| D          |  Hydrogen        | Ni, Fe | K14087  |
| D          |  Hydrogen/CO2    | Mo, W  | K05299  |
| D          |  Ammonia/Methane | Cu     | K10944  |
| A,D        |  Sulfur          | Fe     | K16952  |
| D          |  Thiosulfate     | Fe     | K19713  |
| D          |  CO              | CuMo   | K03520  |
                                                  
                                                  
This module will allow you to compute two indexes:
                                                   
- RMI or Redox-Metabolic Index:
    Is calcualted as the logarithm of the product bewtween the total number of unique donors biogeoSubstrate (energyRole = D)
    KOs and the total number of unique acceptors biogeoSubstrate (energyRole = A) and is defined as:  
    ---> RMI = log(len(set(num_donors))) + log(len(set(num_acceptors))) \n

- MPI or Metal-Plasticity Index 
    Is computed as the number of unique metal pairs scored from previous index, such that Donors (Fe,Ni) and Acceptors (Fe,Ni)
    ,the resulting unique paris will be (Fe,Fe), (Fe,Ni), (Ni,Ni)
    ---> MPI = log(len(set(pairs))) \n

Please, provide a custom table with this information to include it in the geomosaic database and use it for metal index annotation.
""")
