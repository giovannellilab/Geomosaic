from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from geomosaic._utils import GEOMOSAIC_DESCRIPTION
from geomosaic.geo_infer import geo_infer
from geomosaic.geo_setup import geo_setup
from geomosaic.geo_workflow import geo_workflow
from geomosaic.geo_unit import geo_unit


def main():
    parser = ArgumentParser(description=GEOMOSAIC_DESCRIPTION, 
                            formatter_class=ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(title="commands")

    # Creating subcommands for geomosaic
    infer_parser = subparsers.add_parser("infer", help="this command it will help the user to create a \
                                         sample table needed for geomosaic to prepare the working directory",
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    setup_parser = subparsers.add_parser("setup", help="this command creates the working directory for geomosaic, \
                                         and the relative sample folder based on the sample table provided by the user",
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    workflow_parser = subparsers.add_parser("workflow", help="this command allow the user to choose the desired \
                                            modules and the relative packages, then it will create a graph of the modules and start the execution",
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    unit_parser = subparsers.add_parser("unit", help="this command allow the user to choose and run just one module \
                                        in order execute an alternative package for that module",
                                         formatter_class=ArgumentDefaultsHelpFormatter)
    

    # Adding parameters for each subcommamd
    ######################
    ## INFER Parameters ##
    ######################
    infer_parser.add_argument("-d", "--directory", required=True, type=str, help="Path to the directory containing raw reads (fastq.gz files)")
    infer_parser.add_argument("-o", "--output_file", required=False, type=str, default="geomosaic_sample_table.xlsx", help="Output filenameof the sample table")
    infer_parser.add_argument("-s", "--split_token", required=False, type=str, default="_R1_,_R2_", 
                        help="Part of the string filename that help to recognize paired end reads.\
                        It need to be a string, comma separated with no space and two occurrences e.g _R1,_R2  or  R1_,R2_ .\
                        It is also recommended to don't use 'R1' and 'R2' without any symbol, \
                        cause 'R1' and 'R2' can occur also in the section of the filename that means the filename.")
    ## INFER set defaut function
    infer_parser.set_defaults(func=geo_infer)

    ######################
    ## SETUP Parameters ##
    ######################
    setup_parser.add_argument("-d", "--directory", required=True, type=str, help="Path to the directory containing raw reads (fastq.gz files)")
    setup_parser.add_argument("-s", "--sample_table", required=True, type=str, help="Path to the user sample table")
    setup_parser.add_argument("-w", "--working_dir", required=False, default=".", type=str, help="Path where geomosaic can create its working directory")
    setup_parser.add_argument("-c", "--config_file", required=False, default="geomosaic_setup_config.yaml", type=str, 
                              help="Output name for the geomosaic config file (yaml extension). \
                                This file is necessary for the < geomosaic workflow > command.")
    ## SETUP set default function
    setup_parser.set_defaults(func=geo_setup)

    #########################
    ## WORKFLOW Parameters ##
    #########################
    workflow_parser.add_argument("-c", "--config_file", required=True, default="geomosaic_setup_config.yaml", type=str, 
                              help="Path and output filename for the geomosaic config file (yaml extension).")
    workflow_parser.add_argument('-p' ,'--pipeline', action='store_true', help="Execute the default pipeline of geomosaic.")
    ## WORKFLOW set default function
    workflow_parser.set_defaults(func=geo_workflow)

    #####################
    ## UNIT Parameters ##
    #####################
    unit_parser.add_argument("-c", "--config_file", required=True, default="geomosaic_setup_config.yaml", type=str, 
                              help="Path and output filename for the geomosaic config file (yaml extension).")
    unit_parser.add_argument("-m", "--module", required=True, default=None, type=str, 
                              help="Path and output filename for the geomosaic config file (yaml extension).")
    ## WORKFLOW set default function
    unit_parser.set_defaults(func=geo_unit)

    args = parser.parse_args()
    args.func(args)
