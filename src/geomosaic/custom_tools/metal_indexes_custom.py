import os
import re
import pandas as pd
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROMPT
from geomosaic._validator import check_special_characters_on_string


def check_file(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.tsv':
        print(f"Loading {file_path} as TSV...")
        return pd.read_csv(file_path, sep='\t')
    
    elif ext == '.csv':
        print(f"Loading {file_path} as CSV...")
        return pd.read_csv(file_path, sep=',')
    
    elif ext in ['.xlsx', '.xls']:
        print(f"Loading {file_path} as Excel...")
        # Note: Requires 'openpyxl' library installed
        return pd.read_excel(file_path)
    
    else:
        # Fallback: try to "sniff" the delimiter if extension is unknown
        print(f"Unknown extension {ext}. Attempting TSV sniff...")
        return pd.read_csv(file_path, sep='\t')


def validator_metalindex_file(df:str):

    required_cols = ["energyRole", "biogeoSubstrate", "Metal", "KO"]
    missing = set(required_cols) - set(df.columns)

    if missing != None:
        print(f"{GEOMOSAIC_ERROR}: the provided tsv table {str(repr(tsv_file))} does not contain minimal the required columns {required_cols}\n\
              Please, include missing columns {missing}")
        return False
    

    na1 = '^K\d{5}$'
    na2 = '^[AD](\s*,\s*[AD])*$'

    invalid_kos = df[~df['KO'].astype(str).str.match(na2)]

    if invalid_kos:
        print(f"{GEOMOSAIC_ERROR}: the provided tsv table {str(repr(tsv_file))} does not contain the required columns \n\
              Please, provide minimal requested columns: {invalid_kos}")
        return False


    invalid_enrgyrole = df[~df['energyRole'].astype(str).str.match(na2)]

    if invalid_enrgyrole:
        print(f"{GEOMOSAIC_ERROR}: the provided tsv table {str(repr(tsv_file))} does not contain the required columns \n\
              Please, provide minimal requested columns: {invalid_enrgyrole}")
        return False


    return True

