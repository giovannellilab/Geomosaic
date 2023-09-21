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

GEOMOSAIC_DESCRIPTION = f"{bcolors.BOLD}GeoMosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis{bcolors.ENDC}"

GEOMOSAIC_ERROR     = f"{bcolors.FAIL}GeoMosaic Error{bcolors.ENDC}"
GEOMOSAIC_WARNING   = f"{bcolors.WARNING}GeoMosaic Warning{bcolors.ENDC}"
GEOMOSAIC_NOTE      = f"{bcolors.OKBLUE}GeoMosaic Note{bcolors.ENDC}"
GEOMOSAIC_PROCESS   = f"{bcolors.HEADER}GeoMosaic Process{bcolors.ENDC}"

GEOMOSAIC_OK        = f"{bcolors.OKGREEN}OK{bcolors.ENDC}"
