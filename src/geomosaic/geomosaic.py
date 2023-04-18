from argparse import ArgumentParser
from geomosaic.user_choices import get_user_choices
from subprocess import check_call
from geomosaic.validator import validate_working_dir


def main():
    args = parse_args()

    folder_raw_reads = args.directory
    working_dir = args.working_dir
    sample_table = args.sample_table

    pipeline = args.pipeline

    validate_working_dir(working_dir)

    # init
    geomosaic_dir = f"{working_dir}/geomosaic"
    check_call(f"mkdir -p {geomosaic_dir}", shell=True)

    get_user_choices(folder_raw_reads, geomosaic_dir, sample_table, pipeline)


def echo_geomosaic():
    print("GeoMosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis")


def parse_args():
    parser = ArgumentParser(description="GeoMosaic: A flexible metagenomic pipeline combining read-based, assemblies and MAGs with downstream analysis")

    parser.add_argument("-d", "--directory", required=True, type=str, help="Path to the directory containing raw reads (fastq.gz files)")
    parser.add_argument("-w", "--working_dir", required=True, default=".", type=str, help="Path to the working directory for geomosaic")
    parser.add_argument("-s", "--sample_table", required=True, type=str, help="Path to the user sample table")
    parser.add_argument('-p' ,'--pipeline', action='store_true', help="Default pipeline of geomosaic")
    
    return parser.parse_args()
