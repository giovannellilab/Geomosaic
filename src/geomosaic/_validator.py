
import os
from geomosaic._utils import GEOMOSAIC_ERROR
import re


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


def validator_hmmsearch_output_folder(param, additional_parameters):
    check = check_special_characters_on_string(param)

    if not check:
        return False

    if "assembly_hmmsearch_output_folder" in additional_parameters and param == additional_parameters["assembly_hmmsearch_output_folder"]:
        print(f"{GEOMOSAIC_ERROR}: The provided name has already been used for 'assembly_hmmsearch_output_folder'.")
        return False

    if "mags_hmmsearch_output_folder" in additional_parameters and param == additional_parameters["mags_hmmsearch_output_folder"]:
        print(f"{GEOMOSAIC_ERROR}: The provided name has already been used for 'mags_hmmsearch_output_folder'.")
        return False

    return True


def check_special_characters_on_string(s):
    # Make own character set and pass 
    # this as argument in compile method    
    na1 = ',["@!#$%^&*()<>?/\|}{~:;]'
    na2 = "'`€¹²³¼½¬="

    regex1 = re.compile(na1)
    regex2 = re.compile(na2)
     
    # Pass the string in search method of regex object.    
    if(regex1.search(s) != None):
        print(f"{GEOMOSAIC_ERROR}: Your provided output folder name contains a special character that is not allowed: {str(repr(s))}\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False

    if(regex2.search(s) != None):
        print(f"{GEOMOSAIC_ERROR}: Your provided output folder name contains a special character that is not allowed: {str(repr(s))}\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False
    
    if " " in s:
        print(f"{GEOMOSAIC_ERROR}: Your provided output folder name contains a space which is not allowed: {str(repr(s))}.\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False

    if s == "":
        print(f"{GEOMOSAIC_ERROR}: Your provided output folder name cannot be None as: {str(repr(s))}.\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False

    return True
