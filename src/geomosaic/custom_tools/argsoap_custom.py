import os
import re
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_PROMPT
from geomosaic._validator import check_special_characters_on_string


def prepare_argsoap_customdb(config_customdb_section, config_extdb_section, collected_info, geomosaic_externaldb_folder):
    # USER FILES
    config_customdb_section["user_protein_fasta"] = collected_info["argsoap_custom_protein_fasta"]
    config_customdb_section["user_mapping_file"] = collected_info["argsoap_custom_mapping_file"]
    config_customdb_section["output_folder"] = collected_info["argsoap_custom_output_folder"]

    basename_fasta = os.path.basename(collected_info["argsoap_custom_protein_fasta"])
    basename_mapping = os.path.basename(collected_info["argsoap_custom_mapping_file"])

    # EXTDB Section
    config_extdb_section["database_folder"] = os.path.join(geomosaic_externaldb_folder, collected_info["argsoap_custom_database_folder"])
    config_extdb_section["protein_fasta"] = os.path.join(geomosaic_externaldb_folder, collected_info["argsoap_custom_database_folder"], basename_fasta)
    config_extdb_section["mapping_file"] = os.path.join(geomosaic_externaldb_folder, collected_info["argsoap_custom_database_folder"], basename_mapping)


def validator_argsoap_fastafile(fasta_file):
    # Make own character set and pass 
    # this as argument in compile method    
    na1 = ',["@!#$%^&*()<>?/\|}{~:;]'
    na2 = "'`€¹²³¼½¬="

    regex1 = re.compile(na1)
    regex2 = re.compile(na2)

    if " " in fasta_file:
        print(f"{GEOMOSAIC_ERROR}: the provided fasta file {str(repr(fasta_file))} does contain a space. To avoid later issues, please rename the file without any space.")
        return False
    
    if(regex1.search(fasta_file) != None):
        print(f"{GEOMOSAIC_ERROR}: the provided fasta file does contain a special character that is not allowed: {str(repr(fasta_file))}\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False

    if(regex2.search(fasta_file) != None):
        print(f"{GEOMOSAIC_ERROR}: the provided fasta file does contain a special character that is not allowed: {str(repr(fasta_file))}\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False
    
    # Check if the file exists
    if not os.path.exists(fasta_file):
        print(f"{GEOMOSAIC_ERROR}: the provided fasta file does not exist.")
        return False

    return True


def validator_argsoap_mapping(mapping_file):
    # Make own character set and pass 
    # this as argument in compile method    
    na1 = ',["@!#$%^&*()<>?/\|}{~:;]'
    na2 = "'`€¹²³¼½¬="

    regex1 = re.compile(na1)
    regex2 = re.compile(na2)

    if " " in mapping_file:
        print(f"{GEOMOSAIC_ERROR}: the provided mapping file {str(repr(mapping_file))} does contain a space. To avoid later issues, please rename the file without any space.")
        return False
    
    if(regex1.search(mapping_file) != None):
        print(f"{GEOMOSAIC_ERROR}: the provided mapping file does contain a special character that is not allowed: {str(repr(mapping_file))}\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False

    if(regex2.search(mapping_file) != None):
        print(f"{GEOMOSAIC_ERROR}: the provided mapping file does contain a special character that is not allowed: {str(repr(mapping_file))}\n\
              The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
        return False
    
    # Check if the file exists
    if not os.path.exists(mapping_file):
        print(f"{GEOMOSAIC_ERROR}: the provided mapping file does not exist.")
        return False

    with open(os.path.abspath(mapping_file)) as fd:
        header = next(fd)
        
        columns = header.rstrip("\n").split("\t")
        for c in columns:
            if " " in c:
                print(f"{GEOMOSAIC_ERROR}: the provided column name {str(repr(c))} in the mapping file does contain a space. To avoid later issues, please rename or replace the space with '_'")
                return False
            
            if(regex1.search(c) != None):
                print(f"{GEOMOSAIC_ERROR}: the provided column name {str(repr(c))} in the mapping file does contain a special character that is not allowed: {str(repr(mapping_file))}\n\
                    The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
                return False
            
            if(regex2.search(c) != None):
                print(f"{GEOMOSAIC_ERROR}: the provided column name {str(repr(c))} in the mapping file does contain a special character that is not allowed: {str(repr(mapping_file))}\n\
                    The following special characters are not allowed: {na1[0]} {na1[1:]}{na2}")
                return False

    return True


def validator_argsoap_outfolder(param):
    check = check_special_characters_on_string(param)

    if not check:
        return False

    return True


def validator_argsoap_database(param):
    check = check_special_characters_on_string(param)

    if not check:
        return False

    return True


argsoap_database_structure = GEOMOSAIC_PROMPT("""
#######################################
#### ARGs-OAP Custom Database Info ####
#######################################

### Please read all the content below.

For detailed documentation, please refer to the ARGs-OAP Repository: https://github.com/xinehc/args_oap

I will try to simplify based also on my experience using this tool. Moreover some checks will be performed on the provided files to avoid later issues with the code. 

You need two files:

- A fasta file of protein sequences, named for example 'sequences.fasta' (Do not put space in the filename).
We suggest to make this file as simple as possible. The header of each sequence should contain just the ID without any space, tab, or other irregular characters such as forward slash.
Avoid duplicated headers and duplicated sequences.

sequences.fasta:

    >id1
    DQEATRFKT...
    >id2
    GWTRCMDCQ...

- A file named 'mapping.tsv', which is tab-separated. 
This file should contain at least one column, describing all the IDs of the fasta sequences. 
However you can put more columns, each one representing Class, Subclass or categories of your interests.
Do not put space in the column name. We suggest putting "_" instead of spaces. Geomosaic will make some checks.

mapping.tsv:

    IDs    Class    Subclass    Metal_Resistances
    id1    class1    subclass1    iron
    id2    class2    subclass2    iron

""")

