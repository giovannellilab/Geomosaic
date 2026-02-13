import os
import re
import pandas as pd
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROMPT
from geomosaic._validator import check_special_characters_on_string


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

    if not os.path.exists(file_path):
        print(f"{GEOMOSAIC_ERROR}: the provided file does not exist.")
        return False


    df, extension, f_name = check_file(file_path)

    required_cols = ["energyRole", "biogeoSubstrate", "Metal", "KO"]
    missing = set(required_cols) - set(df.columns)

    if missing != None:
        print(f"{GEOMOSAIC_ERROR}: the provided {extension} table {str(repr(f_name))} does not contain minimal the required columns {required_cols}\n\
              Please, include missing columns {missing}")
        return False
    

    na3 = '^K\d{5}$'
    na4 = '^[AD](\s*,\s*[AD])*$'

    invalid_kos = df[~df['KO'].astype(str).str.match(na3)]

    if invalid_kos:
        print(f"{GEOMOSAIC_ERROR}: the provided {extension} table {str(repr(f_name))} does not contain the required columns \n\
              Please, provide minimal requested columns: {invalid_kos}")
        return False


    invalid_enrgyrole = df[~df['energyRole'].astype(str).str.match(na2)]

    if invalid_enrgyrole:
        print(f"{GEOMOSAIC_ERROR}: the provided {extension} table {str(repr(f_name))} does not contain the required columns \n\
              Please, provide minimal requested columns: {invalid_enrgyrole}")
        return False

    return True


metal_indexes_structure = GEOMOSAIC_PROMPT("""METAL INDEX CUSTOM MODULE:\n\
This module allows you to provide a custom table with metal indexes information. \n\
The table must be in .tsv, .csv or .xlsx format and must contain the following columns: energyRole, biogeoSubstrate, Metal, KO. \n\
The energyRole column must contain the energy role of the metal index (e.g., A for acceptor, D for donor). \n\
The biogeoSubstrate column must contain the biogeochemi)cal substrate associated with the metal index (e.g., Fe, Mn, S). \n\
The Metal column must contain the name of the metal associated with the index (e.g., Iron, Manganese, Sulfur). \n\
The KO column must contain the KEGG Orthology (KO) identifier associated with the metal index (e.g., K00001). \n\
Please, provide a custom table with this information to include it in the geomosaic database and use it for metal index annotation.""")