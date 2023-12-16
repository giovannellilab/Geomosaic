from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter
from geomosaic._utils import GEOMOSAIC_DESCRIPTION, GEOMOSAIC_MODULES_DESCRIPTION, GEOMOSAIC_MODULES
from geomosaic.gm_setup import geo_setup
from geomosaic.gm_workflow import geo_workflow
from geomosaic.gm_unit import geo_unit
from geomosaic.gm_envinstall import geo_envinstall
from pathlib import Path
import sys
import pathlib


def main():
    parser = ArgumentParser(description=GEOMOSAIC_DESCRIPTION, 
                            formatter_class=ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(title="commands")

    # Creating subcommands for geomosaic
    # infer_parser = subparsers.add_parser("infer", help="this command it will help the user to create a \
    #                                      sample table needed for geomosaic to prepare the working directory",
    #                                      formatter_class=ArgumentDefaultsHelpFormatter)
    setup_parser = subparsers.add_parser("setup", help="It creates the geomosaic working directory \
                                         and the relative samples folders based on the provided sample table",
                                         formatter_class=ArgumentDefaultsHelpFormatter,
                                         add_help=False)
    workflow_parser = subparsers.add_parser("workflow", help="It allows to choose the desired \
                                            modules and the relative packages. Based on you choices, the command will create a Snakefile (in the geomosaic directory) with the chosen modules, the config file for snakemake, and a graph image to show the created workflow",
                                         formatter_class=RawDescriptionHelpFormatter,
                                         add_help=False)
    unit_parser = subparsers.add_parser("unit", help="It allows to choose and run just one module, for example \
                                        to execute an alternative package for that module. The command create another Snakefile a config file (both in the geomosaic directory) with the chosen module",
                                         formatter_class=RawDescriptionHelpFormatter,
                                         add_help=False)
    envinstall_parser = subparsers.add_parser("envinstall", help="It will installation the required conda environments of your workflow/unit.",
                                         formatter_class=RawDescriptionHelpFormatter,
                                         add_help=False)
    # run_parser = subparsers.add_parser("run", help="Execute the create snakefile",
    #                                      formatter_class=ArgumentDefaultsHelpFormatter,
    #                                      add_help=False)
    

    # Adding parameters for each subcommamd
    ######################
    ## INFER Parameters ##
    ######################
    # infer_parser.add_argument("-d", "--directory", required=True, type=str, help="Path to the directory containing raw reads (fastq.gz files)")
    # infer_parser.add_argument("-o", "--output_file", required=False, type=str, default="geomosaic_sample_table.xlsx", help="Output filenameof the sample table")
    # infer_parser.add_argument("-s", "--split_token", required=False, type=str, default="_R1_,_R2_", 
    #                     help="Part of the string filename that help to recognize paired end reads.\
    #                     It need to be a string, comma separated with no space and two occurrences e.g _R1,_R2  or  R1_,R2_ .\
    #                     It is also recommended to don't use 'R1' and 'R2' without any symbol, \
    #                     cause 'R1' and 'R2' can occur also in the section of the filename that means the filename.")
    # ## INFER set defaut function
    # infer_parser.set_defaults(func=geo_infer)

    ######################
    ## SETUP Parameters ## 
    ######################
    setup_required = setup_parser.add_argument_group("Required Arguments")
    setup_required.add_argument("-d", "--directory", required=True, type=str, help="Path to the directory containing raw reads (fastq.gz files)")
    setup_required.add_argument("-t", "--sample_table", required=True, type=str, help="Path to the user sample table")

    setup_optional = setup_parser.add_argument_group("Optional Arguments")
    setup_optional.add_argument("-s", "--setup_file", required=False, default="gmsetup.yaml", type=str, 
                              help="Output name for the geomosaic setup file (yaml extension). \
                                This file is necessary for the < geomosaic workflow > command.")
    setup_optional.add_argument("-f", "--format_table", required=False, default="tsv", type=str, choices=["tsv", "csv", "excel"],
                              help="Format of the provided table. Allowed: tsv, csv, excel")
    setup_optional.add_argument("-w", "--working_dir", required=False, default="geomosaic", type=str, help="Path where geomosaic can create its working directory. Default: './geomosaic' ")
    setup_optional.add_argument("-n", "--project_name", required=False, default="Geomosaic_Workflow", type=str, help="Name of the project (no-space)")
    setup_optional.add_argument('--skip_wdir_checks', action='store_true', required=False,  help="")
    setup_optional.add_argument('--nocopy', action='store_true', required=False,  help="Suggested flag if the provided raw reads directory is an already backup of the original files. \
                              In this case, geomosaic will create only symbolic link of raw reads to its working directory. Note: This flag cannot be used if \
                              there are multiple files for each R1 and R2 sample reads, as geomosaic will 'cat' them to a single file.")
    
    setup_help = setup_parser.add_argument_group("Help Arguments")
    setup_help.add_argument("-h", "--help", action="help", help="show this help message and exit")
    ## SETUP set default function
    setup_parser.set_defaults(func=geo_setup)

    #########################
    ## WORKFLOW Parameters ##
    #########################
    workflow_required = workflow_parser.add_argument_group("Required Arguments")
    workflow_required.add_argument("-s", "--setup_file", required=True, type=str, 
                              help="Geomosaic setup file created from the 'geomosaic setup ...' command.")
    
    workflow_optional = workflow_parser.add_argument_group("Optional Arguments")
    workflow_optional.add_argument('-t' ,'--threads', default=10, type=int, help="Threads to use (per sample).")
    workflow_optional.add_argument('-e' ,'--externaldb_gmfolder', default=None,type=lambda p: pathlib.Path(p).resolve(),
                                   help="If you have already downloaded and setup \
                                   databases with geomosaic, here you can specify the path folder.")
    workflow_optional.add_argument('-g' ,'--glab', action='store_true', help="Execute the default Giovannelli's Lab pipeline of Geomosaic.")
    workflow_optional.add_argument("-m", "--module_start", required=False, type=str, default="pre_processing",
                                help=f"Module where to start creating the workflow (Default: pre_processing)", choices=GEOMOSAIC_MODULES, metavar="MODULE")
    
    workflow_parser.add_argument_group("Available Modules", GEOMOSAIC_MODULES_DESCRIPTION)
    
    workflow_help = workflow_parser.add_argument_group("Help Arguments")
    workflow_help.add_argument("-h", "--help", action="help", help="show this help message and exit")
    ## WORKFLOW set default function
    workflow_parser.set_defaults(func=geo_workflow)

    #####################
    ## UNIT Parameters ##
    #####################
    
    unit_required = unit_parser.add_argument_group("Required Arguments")
    unit_required.add_argument("-s", "--setup_file", required=True, type=str, 
                                help="Geomosaic setup file created from the 'geomosaic setup ...' command.")
    unit_required.add_argument("-m", "--module", required=True, type=str, 
                                help=f"Modules to execute.", choices=GEOMOSAIC_MODULES, metavar="MODULE")
    unit_optional = unit_parser.add_argument_group("Optional Arguments")
    unit_optional.add_argument('-t' ,'--threads', default=10, type=int, help="Threads to use (per sample).")
    unit_optional.add_argument('-e' ,'--externaldb_gmfolder', default=None,type=lambda p: pathlib.Path(p).resolve(),
                                   help="If you have already downloaded and setup \
                                   databases with geomosaic, here you can specify the path folder.")
    
    unit_parser.add_argument_group("Available Modules", GEOMOSAIC_MODULES_DESCRIPTION)

    unit_help = unit_parser.add_argument_group("Help Arguments")
    unit_help.add_argument("-h", "--help", action="help", help=f"show this help message and exit")
    ## unit set default function
    unit_parser.set_defaults(func=geo_unit)


    #####################
    ## ENVINSTALL Parameters ##
    #####################

    envinstall_required = envinstall_parser.add_argument_group("Required Arguments")
    envinstall_required.add_argument("-s", "--setup_file", required=True, type=str, 
                                help="Geomosaic setup file created from the 'geomosaic setup ...' command.")
    envinstall_optional = envinstall_parser.add_argument_group("Optional Arguments")
    envinstall_optional.add_argument('-u' ,'--unit', action='store_true', help="Install the conda environment of your geomosaic unit.")

    envinstall_help = envinstall_parser.add_argument_group("Help Arguments")
    envinstall_help.add_argument("-h", "--help", action="help", help=f"show this help message and exit")
    ## envinstall set default function
    envinstall_parser.set_defaults(func=geo_envinstall)


    # envinstall_parser
    ####################
    ## RUN Parameters ##
    ####################
    # run_parser.add_argument("-c", "--config_file", required=True, default="geomosaic_setup_config.yaml", type=str, 
    #                           help="Path and output filename for the geomosaic config file (yaml extension).")
    # run_parser.add_argument("-t", "--threads", required=True, default=8, help="Number of threads to use to execute the workflow for all the samples")
    # run_parser.add_argument("-s", "--threads_per_sample", required=True, default=4, help="Threads to use per each sample. It must be lower than the 'threads' \
    #                         parameter")

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)
