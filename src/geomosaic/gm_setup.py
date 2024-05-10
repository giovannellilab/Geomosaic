import os
import pandas as pd
import yaml
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_NOTE, GEOMOSAIC_OK, GEOMOSAIC_PROCESS, GEOMOSAIC_PROMPT, GEOMOSAIC_WARNING
from geomosaic._validator import validate_working_dir
import pkg_resources
import time
import shutil
import re
from subprocess import check_call
from tqdm import tqdm


def geo_setup(args):
    folder_raw_reads    = args.directory
    working_dir         = args.working_dir
    sample_table        = args.sample_table
    setup_file          = args.setup_file
    project_name        = args.project_name
    move_and_rename     = args.move_and_rename
    format_table        = args.format_table
    skip_checks         = args.skip_checks

    if not os.path.isdir(working_dir):
        os.makedirs(working_dir)
    else:
        print(f"{GEOMOSAIC_ERROR}: In the provided path '{working_dir}' a geomosaic folder already exists")
        exit(1)

    geo_wdir = os.path.abspath(working_dir)
    
    print(f"{GEOMOSAIC_PROCESS}: Mapping samples to filenames... ", end="", flush=True)
    samples_list = group_read_by_sample(
        filename        = sample_table,
        format          = format_table,
        rawreads_folder = os.path.abspath(folder_raw_reads),
        wdir            = geo_wdir,
        move_and_rename = move_and_rename,
        skip_checks     = skip_checks
    )
    time.sleep(5)
    print(GEOMOSAIC_OK)
    
    config_parameters = {
        "PROJECT_NAME": project_name,
        "GEOMOSAIC_VERSION": pkg_resources.get_distribution("geomosaic").version,
        "GEOMOSAIC_WDIR": geo_wdir,
        "USER_RAWREADS_DIRECTORY": os.path.abspath(folder_raw_reads),
        "PROJECT_DESCRIPTION": "Metagenomics pipeline with GeoMosaic.",
        "SAMPLES": samples_list,
    }
    
    with open(setup_file, 'w') as fd_config:
        yaml.dump(config_parameters, fd_config, sort_keys=False)

    prompt1 = GEOMOSAIC_PROMPT(f"geomosaic workflow -s {os.path.abspath(setup_file)}")
    prompt2 = GEOMOSAIC_PROMPT(f"geomosaic workflow --help")
    print(f"\n{GEOMOSAIC_NOTE}: the geomosaic setup file has been created in the following path:\n{os.path.abspath(setup_file)}")
    print(f"\n{GEOMOSAIC_NOTE}: You can now create your pipeline (or use the default one) by executing:\n{prompt1}\nHowever, we suggest you to use\n{prompt2}\nto required and optional parameters.\n")


def group_read_by_sample(filename, format, rawreads_folder, wdir, move_and_rename, skip_checks):
    rawreads_container = list(os.listdir(rawreads_folder))

    if format == "tsv":
        df = pd.read_csv(filename, sep="\t")
    elif format == "csv":
        df = pd.read_csv(filename, sep=",")
    else:
        df = pd.read_excel(filename)
    
    assert list(df.columns) == ["r1", "r2", "sample"], f"\n\n{GEOMOSAIC_ERROR}: the provided table should contains three columns, with the following header all lower-case: r1 r2 sample"

    if not skip_checks:
        for i in df.itertuples():
            check_special_characters(i.sample)
            check_space_reads(i.r1)
            check_space_reads(i.r2)
            check_presence_read(i.r1, rawreads_container)
            check_presence_read(i.r2, rawreads_container)

    grp = df.groupby(by="sample").agg(list)
    grp.reset_index(inplace=True)
    
    for i in list(grp.itertuples()):
        if move_and_rename:
            if len(i.r1) > 1 or len(i.r2) > 1:
                print(f"{GEOMOSAIC_ERROR}: '--move_and_rename' flag cannot be used as there are multiple reads file for the sample '{i.sample}'.")
                exit(1)
        
    samples_list = []

    for i in tqdm(list(grp.itertuples())):
        samples_list.append(i.sample)
        check_call(f"mkdir -p {os.path.join(wdir, i.sample)}", shell=True)

        if move_and_rename:
            assert len(i.r1) == 1, f"{GEOMOSAIC_ERROR}: '--move_and_rename' flag cannot be used when there are multiple reads file for one sample '{i.sample}'."
            assert len(i.r2) == 1, f"{GEOMOSAIC_ERROR}: '--move_and_rename' flag cannot be used when there are multiple reads file for one sample '{i.sample}'."

            shutil.move(os.path.join(rawreads_folder, i.r1[0]), os.path.join(wdir, i.sample, "R1.fastq.gz"))
            shutil.move(os.path.join(rawreads_folder, i.r2[0]), os.path.join(wdir, i.sample, "R2.fastq.gz"))
        
        else:
            all_r1 = " ".join([os.path.join(rawreads_folder,x) for x in i.r1])
            all_r2 = " ".join([os.path.join(rawreads_folder,x) for x in i.r2])

            check_call(f"cat {all_r1} > {os.path.join(wdir, str(i.sample), 'R1.fastq.gz')}", shell=True)
            check_call(f"cat {all_r2} > {os.path.join(wdir, str(i.sample), 'R2.fastq.gz')}", shell=True)
    
    return samples_list


def check_special_characters(s):
    # Make own character set and pass 
    # this as argument in compile method    
    na1 = ',["@!#$%^&*()<>?/\|}{~:;]'
    na2 = "'`€¹²³¼½¬="

    regex1 = re.compile(na1)
    regex2 = re.compile(na2)
     
    # Pass the string in search 
    # method of regex object.    
    if(regex1.search(s) != None):
        print(f"{GEOMOSAIC_ERROR}: Your sample name contains a special character that is not allowed: {str(repr(s))}\n\
              The following special characters are not allowed in sample name: {na1[0]} {na1[1:]}{na2}")
        exit(1)

    if(regex2.search(s) != None):
        print(f"{GEOMOSAIC_ERROR}: Your sample name contains a special character that is not allowed: {str(repr(s))}\n\
              The following special characters are not allowed in sample name: {na1[0]} {na1[1:]}{na2}")
        exit(1)
    
    if " " in s:
        print(f"{GEOMOSAIC_ERROR}: Your sample name contains a space which is not allowed: {str(repr(s))}.\n\
              The following special characters are not allowed in sample name: {na1[0]} {na1[1:]}{na2}")
        exit(1)


def check_space_reads(r):
    if " " in r:
        print(f"{GEOMOSAIC_ERROR}: Your read name contains a space which may create problems: {str(repr(r))}.\n\
              Please rename the read filename.")
        exit(1)


def check_presence_read(r, f):
    if r not in f:
        print(f"{GEOMOSAIC_ERROR}: The following read file {str(repr(r))} in the provided table is not present in the folder {str(repr(f))}\n\
              Re-check if the folder of the rawreads does contain all the reads.")
        exit(1)
