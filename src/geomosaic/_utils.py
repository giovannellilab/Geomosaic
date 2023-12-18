import os
import json


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def read_modules(description: bool):
    gmpackages_path = os.path.join(os.path.dirname(__file__), 'gmpackages.json')

    with open(gmpackages_path, 'rt') as f:
        gmpackages = json.load(f)
    
    descr_available_moules = "\n"
    available_moules = []
    for m, v in gmpackages["modules"].items():
        descr_available_moules += f"- {bcolors.OKBLUE}{m}{bcolors.ENDC} - {v['description']}\n"
        available_moules.append(m)
    
    if description:
        return descr_available_moules
    else:
        return available_moules


GEOMOSAIC_DESCRIPTION = f"{bcolors.BOLD}Geomosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis{bcolors.ENDC}"

GEOMOSAIC_ERROR     = f"{bcolors.FAIL}Geomosaic Error{bcolors.ENDC}"
GEOMOSAIC_WARNING   = f"{bcolors.WARNING}Geomosaic Warning{bcolors.ENDC}"
GEOMOSAIC_NOTE      = f"{bcolors.OKBLUE}Geomosaic Note{bcolors.ENDC}"
GEOMOSAIC_PROCESS   = f"{bcolors.HEADER}Geomosaic Process{bcolors.ENDC}"

def GEOMOSAIC_PROMPT(command):
    return f"{bcolors.BOLD}{command}{bcolors.ENDC}"

GEOMOSAIC_OK        = f"\n--> {bcolors.OKGREEN}OK{bcolors.ENDC} <--"

GEOMOSAIC_MODULES_DESCRIPTION = read_modules(description=True)
GEOMOSAIC_MODULES = read_modules(description=False)
