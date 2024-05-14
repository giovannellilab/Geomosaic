import os
import json
import yaml
from argparse import ArgumentError


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


def read_gathering(description: bool):
    gmpackages_path = os.path.join(os.path.dirname(__file__), 'gmpackages.json')

    with open(gmpackages_path, 'rt') as f:
        gmpackages = json.load(f)
    
    descr_available_packages = "\n"
    available_packages = ["_ALL_"]
    for package in gmpackages["gathering"]:
        descr_available_packages += f"- {bcolors.OKBLUE}{package}{bcolors.ENDC}\n"
        available_packages.append(package)
    
    if description:
        return descr_available_packages
    else:
        return available_packages


def csv_values(vstr, sep=','):
    '''
    @returns iterable of string after separated by comma
    '''
    values = []
    for v0 in vstr.split(sep):
        try:
            v = str(v0)
            values.append(v)
        except ValueError as err:
            raise ArgumentError('Invalid value %s' % v)
    return values


GEOMOSAIC_DESCRIPTION = f"{bcolors.BOLD}Geomosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis{bcolors.ENDC}"

GEOMOSAIC_ERROR     = f"{bcolors.FAIL}Geomosaic Error{bcolors.ENDC}"
GEOMOSAIC_WARNING   = f"{bcolors.WARNING}Geomosaic Warning{bcolors.ENDC}"
GEOMOSAIC_NOTE      = f"{bcolors.OKBLUE}Geomosaic Note{bcolors.ENDC}"
GEOMOSAIC_PROCESS   = f"{bcolors.HEADER}Geomosaic Process{bcolors.ENDC}"

def GEOMOSAIC_PROMPT(command):
    return f"{bcolors.BOLD}{command}{bcolors.ENDC}"

GEOMOSAIC_OK = f"\n--> {bcolors.OKGREEN}OK{bcolors.ENDC} <--"

GEOMOSAIC_MODULES_DESCRIPTION = read_modules(description=True)
GEOMOSAIC_MODULES = read_modules(description=False)

GEOMOSAIC_GATHER_PACKAGES = read_gathering(description=False)
GEOMOSAIC_GATHER_PACKAGES_DESCRIPTION = read_gathering(description=True)


def append_to_gmsetupyaml(file_path, data_to_append):
    with open(file_path) as file:
        gmsetup = yaml.load(file, Loader=yaml.FullLoader)
    
    for k, v in data_to_append.items():
        gmsetup[k] = v
    
    with open(file_path, 'w') as fd_config:
        yaml.dump(gmsetup, fd_config, sort_keys=False)
