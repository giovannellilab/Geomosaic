
import os


def validate_working_dir(working_dir):
    if not os.path.exists(working_dir):
        print(f"GeoMosaic Error: Inserted wdir path '{working_dir}' does not exists.")
        exit(code=1)

    if not os.path.isdir(working_dir):
        print(f"GeoMosaic Error: {working_dir} is not a directory")
        exit(code=1)


def validator_hmms_folder(hmms_folder):
    if not os.path.exists(hmms_folder):
        print(f"GeoMosaic Error: inserted folder does not exists.")
        return False

    if not os.path.isdir(hmms_folder):
        print(f"GeoMosaic Error: '{hmms_folder}' is not a directory")
        return False
    
    unique = []
    for f in os.listdir(hmms_folder):
        if not f.endswith(".hmm"):
            print(f"GeoMosaic Error: The file:\n\n'{f}'\n\n inside the folder:\n\n'{hmms_folder}'\n\ndoesn't have the '.hmm' extension.")
            return False
        
        if " " in f:
            print(f"GeoMosaic Error: The file:\n\n'{f}'\n\n inside the folder:\n\n'{hmms_folder}'\n\nseems to have a space in its name.")
            return False
        
        if f in unique:
            print(f"GeoMosaic Error: The file:\n\n'{f}'\n\n inside the folder:\n\n'{hmms_folder}'\n\nseems to be a duplicate.")
            return False

        unique.append(f)

    return True    
