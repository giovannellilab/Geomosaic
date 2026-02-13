import os
import re
import pandas as pd
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROMPT
from geomosaic._validator import check_special_characters_on_string


def check_file(file_path: str):

    ext = os.path.splitext(file_path)[1].lower()
    f_name = os.path.basename(file_path)

    if ext == '.tsv':
        return pd.read_csv(file_path, sep='\t'), ext, f_name
    
    elif ext == '.csv':
        return pd.read_csv(file_path, sep=','), ext, f_name
    
    elif ext in ['.xlsx', '.xls']:
        # Note: Requires 'openpyxl' library installed
        return pd.read_excel(file_path), ext, f_name
    
    else:
        # Fallback: try to "sniff" the delimiter if extension is unknown
        return pd.read_csv(file_path, sep='\t'), ext, f_name


def validator_metalindex_file(file_path:str):

    df, extension, f_name = check_file(file_path)

    required_cols = ["energyRole", "biogeoSubstrate", "Metal", "KO"]
    missing = set(required_cols) - set(df.columns)

    if missing != None:
        print(f"{GEOMOSAIC_ERROR}: the provided {extension} table {str(repr(f_name))} does not contain minimal the required columns {required_cols}\n\
              Please, include missing columns {missing}")
        return False
    
    na1 = '^K\d{5}$'
    na2 = '^[AD](\s*,\s*[AD])*$'

    invalid_kos = df[~df['KO'].astype(str).str.match(na1)]

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


metal_index_file_structure = GEOMOSAIC_PROMPT("""
#######################################
#### RMI-RPI Custom Database Info ####
#######################################

### Please read all the content below.

For detailed documentation, please refer to the ARGs-OAP Repository: https://github.com/xinehc/args_oap

You need to build a table containing

- A fasta file of protein sequences, named for example 'sequences.fasta' (Do not put space in the filename).
We suggest to make this file as simple as possible. The header of each sequence should contain just the ID without any space, tab, or other irregular characters such as forward slash.
Avoid duplicated headers and duplicated sequences.

sequences.fasta:

    >id1
    DQEATRFKT...
    >id2
    GWTRCMDCQ...

- A file of mapping, for example 'mapping.tsv', which is tab-separated. 
This file should contain at least one column, describing all the IDs of the fasta sequences. 
However you can put more columns, each one representing Class, Subclass or categories of your interests.
Do not put space in the column name. We suggest putting "_" instead of spaces. Geomosaic will make some checks.

mapping.tsv:

    IDs    Class    Subclass    Metal_Resistances
    id1    class1    subclass1    iron
    id2    class2    subclass2    iron

""")

