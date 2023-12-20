from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, RawDescriptionHelpFormatter
from geomosaic._utils import GEOMOSAIC_DESCRIPTION, GEOMOSAIC_MODULES_DESCRIPTION, GEOMOSAIC_MODULES, GEOMOSAIC_PROMPT
from geomosaic.gm_setup import geo_setup
from geomosaic.gm_workflow import geo_workflow
from geomosaic.gm_unit import geo_unit
from geomosaic.gm_prerun import geo_prerun
import sys
import pathlib


def main():
    parser = ArgumentParser(description=GEOMOSAIC_DESCRIPTION, 
                            formatter_class=ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers(title="commands")

    setup_parser = subparsers.add_parser("setup", help="It creates the geomosaic working directory and the relative samples folders based on the provided sample table",
                                         description=GEOMOSAIC_PROMPT("DESCRIPTION: It creates the geomosaic working directory and the relative samples folders based on the provided sample table"),
                                         formatter_class=ArgumentDefaultsHelpFormatter,
                                         add_help=False)
    workflow_parser = subparsers.add_parser("workflow", help="It allows to choose the desired modules and the relative packages. Based on you choices, the command will create a Snakefile (in the geomosaic directory) with the chosen modules, the config file for snakemake, and a graph image to show the created workflow",
                                            description=GEOMOSAIC_PROMPT("DESCRIPTION: It allows to choose the desired modules and the relative packages. Based on you choices, the command will create a Snakefile (in the geomosaic directory) with the chosen modules, the config file for snakemake, and a graph image to show the created workflow"),
                                            formatter_class=RawDescriptionHelpFormatter,
                                            add_help=False)
    unit_parser = subparsers.add_parser("unit", help="It allows to choose and run just one module, for example to execute an alternative package for that module. The command create another Snakefile a config file (both in the geomosaic directory) with the chosen module",
                                        description=GEOMOSAIC_PROMPT("DESCRIPTION: It allows to choose and run just one module, for example to execute an alternative package for that module. The command create another Snakefile a config file (both in the geomosaic directory) with the chosen module"),
                                        formatter_class=RawDescriptionHelpFormatter,
                                        add_help=False)
    prerun_parser = subparsers.add_parser("prerun", help="This command it is usefull to install the required conda environments of your workflow/unit and create required scripts to execute Geomosaic on a cluster using SLURM",
                                          description=GEOMOSAIC_PROMPT("DESCRIPTION: This command it is usefull to install the required conda environments of your workflow/unit and create required scripts to execute Geomosaic on a cluster using SLURM"),
                                          formatter_class=RawDescriptionHelpFormatter,
                                          add_help=False)

    ######################
    ## SETUP Parameters ## 
    ######################
    setup_required = setup_parser.add_argument_group(GEOMOSAIC_PROMPT("Required Arguments"))
    setup_required.add_argument("-d", "--directory", required=True, type=str, help="Path to the directory containing raw reads (fastq.gz files)")
    setup_required.add_argument("-t", "--sample_table", required=True, type=str, help="Path to the user sample table")

    setup_optional = setup_parser.add_argument_group(GEOMOSAIC_PROMPT("Optional Arguments"))
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
    
    setup_help = setup_parser.add_argument_group(GEOMOSAIC_PROMPT("Help Arguments"))
    setup_help.add_argument("-h", "--help", action="help", help="show this help message and exit")
    ## SETUP set default function
    setup_parser.set_defaults(func=geo_setup)

    #########################
    ## WORKFLOW Parameters ##
    #########################
    workflow_required = workflow_parser.add_argument_group(GEOMOSAIC_PROMPT("Required Arguments"))
    workflow_required.add_argument("-s", "--setup_file", required=True, type=str, 
                              help="Geomosaic setup file created from the 'geomosaic setup ...' command.")
    
    workflow_optional = workflow_parser.add_argument_group(GEOMOSAIC_PROMPT("Optional Arguments"))
    workflow_optional.add_argument('-t' ,'--threads', default=10, type=int, help="Threads to use (per sample).")
    workflow_optional.add_argument('-e' ,'--externaldb_gmfolder', default=None,type=lambda p: pathlib.Path(p).resolve(),
                                   help="If you have already downloaded and setup \
                                   databases with geomosaic, here you can specify the path folder.")
    workflow_optional.add_argument('-g' ,'--glab', action='store_true', help="Execute the default Giovannelli's Lab pipeline of Geomosaic.")
    workflow_optional.add_argument("-m", "--module_start", required=False, type=str, default="pre_processing",
                                help=f"Module where to start creating the workflow (Default: pre_processing)", choices=GEOMOSAIC_MODULES, metavar="MODULE")
    
    workflow_parser.add_argument_group(GEOMOSAIC_PROMPT("Available Modules"), GEOMOSAIC_MODULES_DESCRIPTION)
    
    workflow_help = workflow_parser.add_argument_group(GEOMOSAIC_PROMPT("Help Arguments"))
    workflow_help.add_argument("-h", "--help", action="help", help="show this help message and exit")
    ## WORKFLOW set default function
    workflow_parser.set_defaults(func=geo_workflow)

    #####################
    ## UNIT Parameters ##
    #####################
    unit_required = unit_parser.add_argument_group(GEOMOSAIC_PROMPT("Required Arguments"))
    unit_required.add_argument("-s", "--setup_file", required=True, type=str, 
                                help="Geomosaic setup file created from the 'geomosaic setup ...' command.")
    unit_required.add_argument("-m", "--module", required=True, type=str, 
                                help=f"Modules to execute.", choices=GEOMOSAIC_MODULES, metavar="MODULE")
    unit_optional = unit_parser.add_argument_group(GEOMOSAIC_PROMPT("Optional Arguments"))
    unit_optional.add_argument('-t' ,'--threads', default=10, type=int, help="Threads to use (per sample).")
    unit_optional.add_argument('-e' ,'--externaldb_gmfolder', default=None,type=lambda p: pathlib.Path(p).resolve(),
                                   help="If you have already downloaded and setup \
                                   databases with geomosaic, here you can specify the path folder.")
    
    unit_parser.add_argument_group(GEOMOSAIC_PROMPT("Available Modules"), GEOMOSAIC_MODULES_DESCRIPTION)

    unit_help = unit_parser.add_argument_group(GEOMOSAIC_PROMPT("Help Arguments"))
    unit_help.add_argument("-h", "--help", action="help", help=f"show this help message and exit")
    ## unit set default function
    unit_parser.set_defaults(func=geo_unit)


    #####################
    ## PRERUN Parameters ##
    #####################

    prerun_required = prerun_parser.add_argument_group(GEOMOSAIC_PROMPT("Required Arguments"))
    prerun_required.add_argument("-s", "--setup_file", required=True, type=str, 
                                help="Geomosaic setup file created from the 'geomosaic setup ...' command.")
    
    prerun_optional = prerun_parser.add_argument_group(GEOMOSAIC_PROMPT("Optional Arguments"))
    prerun_optional.add_argument('-u' ,'--unit', action='store_true', help="Install the conda environment of your geomosaic unit.")

    prerun_optionalslurm = prerun_parser.add_argument_group(GEOMOSAIC_PROMPT("Optional Arguments for SLURM Specification or GNU Parallel"))
    prerun_optionalslurm.add_argument('--exec_type', type=str, default="slurm", choices=["slurm", "gnu_parallel"], help="Use this option to specify how do you want execute geomosaic. If SLURM is available on your cluster we suggest to use '--exec_type slurm', otherwise GNU Parallel will be used ('--exec_type gnu_parallel')." +\
                                      "More details on the Geomosaic Documentation. (Default: slurm)")
    prerun_optionalslurm.add_argument('-t', '--threads', default=10, type=int, help="Threads to use (per sample). This value will override the one specified in the workflow/unit (config file) and thus will replace threads value in the config file. (Available for '--exec_type slurm' or '--exec_type gnu_parallel')")
    prerun_optionalslurm.add_argument('-n', '--n_jobs', default=2, type=int, help="Number of jobs to execute in parallel using GNU Parallel. More details on the Geomosaic Documentation. This option is available only for '--exec_type gnu_parallel'.")
    prerun_optionalslurm.add_argument('-m', '--memory', default=300, type=int, help="Memory specification (in GB) for slurm job. (requires '--exec_type slurm' option)")
    prerun_optionalslurm.add_argument('-p', '--partition', default=None, type=str, help="Partition specification for slurm job in the cluster. (requires '--exec_type slurm' option)")
    prerun_optionalslurm.add_argument('--mail_type', default=None, choices=["NONE", "BEGIN", "END", "FAIL", "REQUEUE", "ALL"], help="Mail type to notify user about occurred even type in slurm. Ignore this option if you are not interested to get(requires '--exec_type slurm' option)")
    prerun_optionalslurm.add_argument('--mail_user', default=None, type=str, help="Email where to to receive slurm notification type specified in '--mail_type'. (requires '--exec_type slurm' option)")
    prerun_optionalslurm.add_argument('-f', '--folder_logs', default=None, type=str, help="Folder for logs files. Default is None, but we suggest you to specify it and if it does not exists, Geomosaic will create it. (Available for '--exec_type slurm' or '--exec_type gnu_parallel')")
    prerun_optionalslurm.add_argument('-l', '--list_sample_output', default="list_samples.txt", type=str, help="Filename where to write the list of samples. Default: list_samples.txt created in the current directory. (Available for '--exec_type slurm' or '--exec_type gnu_parallel')")
    prerun_optionalslurm.add_argument('-o', '--output_script', default=None, type=str, help="Filename for the SLURM or GNU Parallel script. As default it will be created as slurm_geomosaic.sh or parallel_geomosaic in the current directory (depending on the '--exec_type' option). (Available for '--exec_type slurm' or '--exec_type gnu_parallel')")
    prerun_optionalslurm.add_argument('-e', '--extdb_output_script', default=None, type=str, help="Filename for the SLURM or GNU Parallel script to execute external db setup. As default it will be created as slurm_extdb_geomosaic.sh or parallel_extdb_geomosaic.sh in the current directory (depending on the '--exec_type' option). (Available for '--exec_type slurm' or '--exec_type gnu_parallel')")

    prerun_help = prerun_parser.add_argument_group(GEOMOSAIC_PROMPT("Help Arguments"))
    prerun_help.add_argument("-h", "--help", action="help", help=f"show this help message and exit")
    ## prerun set default function
    prerun_parser.set_defaults(func=geo_prerun)

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    args.func(args)
