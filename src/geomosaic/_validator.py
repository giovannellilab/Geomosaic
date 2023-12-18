
import os
from geomosaic._utils import GEOMOSAIC_ERROR


def validate_working_dir(working_dir):
    if not os.path.exists(working_dir):
        print(f"{GEOMOSAIC_ERROR}: Inserted wdir path '{working_dir}' does not exists.")
        exit(code=1)

    if not os.path.isdir(working_dir):
        print(f"{GEOMOSAIC_ERROR}: {working_dir} is not a directory")
        exit(code=1)


def validator_hmms_folder(hmms_folder):
    if not os.path.exists(hmms_folder):
        print(f"{GEOMOSAIC_ERROR}: inserted folder does not exists.")
        return False

    if not os.path.isdir(hmms_folder):
        print(f"{GEOMOSAIC_ERROR}: '{hmms_folder}' is not a directory")
        return False
    
    unique = []
    for f in os.listdir(hmms_folder):
        if not f.endswith(".hmm"):
            print(f"{GEOMOSAIC_ERROR}: The file:\n\n'{f}'\n\n inside the folder:\n\n'{hmms_folder}'\n\ndoesn't have the '.hmm' extension.")
            return False
        
        if " " in f:
            print(f"{GEOMOSAIC_ERROR}: The file:\n\n'{f}'\n\n inside the folder:\n\n'{hmms_folder}'\n\nseems to have a space in its name.")
            return False
        
        if f in unique:
            print(f"{GEOMOSAIC_ERROR}: The file:\n\n'{f}'\n\n inside the folder:\n\n'{hmms_folder}'\n\nseems to be a duplicate.")
            return False

        unique.append(f)

    return True


def validator_completeness_contamination_integer(param):
    try:
        integer_param = int(param)
    except Exception as e:
        print(f"{GEOMOSAIC_ERROR}: cannot convert inserted parameter to integer value.")
        return False

    if not (integer_param <= 100 and integer_param >= 0):
        print(f"{GEOMOSAIC_ERROR}: inserted parameter must be 0 <= X <= 100.")
        return False

    return True
