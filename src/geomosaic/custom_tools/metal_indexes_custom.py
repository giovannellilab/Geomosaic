import os
import re
import pandas as pd
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROMPT, GEOMOSAIC_OK, GEOMOSAIC_NOTE
from geomosaic._validator import check_special_characters_on_string


def prepare_metalindex_customdb(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder):
    # USER FILES
    config_customdb_section["user_metal_table"] = collected_info["metal_index_file_table"]
    basename_table = os.path.basename(collected_info["metal_index_file_table"])
    # EXTDB Section
    config_extdb_section["database_folder"] = os.path.join(geomosaic_externaldb_folder, collected_info["metal_custom_database_folder"])
    config_extdb_section["table_file"] = os.path.join(geomosaic_externaldb_folder, collected_info["metal_custom_database_folder"], basename_table)


def check_file(file_path: str):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.tsv':
        return pd.read_csv(file_path, sep='\t'), ext
    elif ext == '.csv':
        return pd.read_csv(file_path, sep=','), ext
    elif ext in ['.xlsx', '.xls']:
        # Note: Requires 'openpyxl' library installed
        return pd.read_excel(file_path), ext
    else:
        # Fallback: try to "sniff" the delimiter if extension is unknown
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


metal_index_database_structure = GEOMOSAIC_PROMPT("""
#####################################
##### METAL INDEX CUSTOM MODULE ##### 
#####################################
This module allows you to provide a custom table with metal indexes information.
The table must be in .tsv, .csv or .xlsx format and MUST contain the following columns:
energyRole, biogeoSubstrate, Metal, KO.
                                                  
- The energyRole column must contain the energy role of the metal index (e.g., A for acceptor, D for donor).
- The biogeoSubstrate refers to the Acceptor/Donor substrate contain the biogeochemical substrate associated with the metal index (e.g., Fe, Mn, S). \n\
- The Metal column must contain the name of the metal associated with the index (e.g., Iron, Manganese, Sulfur).
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
                                                  
This module will allow you to compute two indexes: the RMI or Redox-Metabolic Index and the RPI or Redox-Plasticity Index:

FORMULA: 
    index = math.log(num_donors) + math.log(num_acceptors)

- The RMI is calcualted as the logarithm of the product bewtween the total number of accpetors (A) KOs and the total number of donors (D) KOs
- The RPI is calculated as the logarithm of the product between the total number of accpetors Metals (A) KO[A][Metal] and the total number of Metal donors (D) KO[D][Metal] \n\

Please, provide a custom table with this information to include it in the geomosaic database and use it for metal index annotation.
""")
