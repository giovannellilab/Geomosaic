import os
import pandas as pd
import yaml
from geomosaic._utils import GEOMOSAIC_ERROR, GEOMOSAIC_NOTE
from geomosaic._validator import validate_working_dir


def geo_setup(args):
    print("Mapping samples to filenames...")

    folder_raw_reads    = args.folder_raw_reads
    working_dir         = args.working_dir
    sample_table        = args.sample_table
    config_file         = args.config_file

    validate_working_dir(working_dir)
    
    samples_list = group_read_by_sample(
        filename        = sample_table,
        rawreads_folder = folder_raw_reads,
        wdir            = working_dir
    )

    geo_wdir = os.path.join(working_dir ,"geomosaic")

    if not os.path.isdir(geo_wdir):
        os.makedirs(geo_wdir)
    else:
        print(f"{GEOMOSAIC_ERROR}: In the provided path '{working_dir}' a geomosaic folder already exists")
        exit(1)
    
    config_parameters = {"SAMPLES": samples_list, "GEOMOSAIC_WDIR": geo_wdir}
    
    with open(config_file, 'w') as fd_config:
        yaml.dump(config_parameters, fd_config)

    print(f"{GEOMOSAIC_NOTE}: the geomosaic config file has been created in the following path:\n{os.path.abspath(config_file)}")


def group_read_by_sample(filename, rawreads_folder, wdir):
    df = pd.read_csv(filename, sep="\t")

    grp = df.groupby(by="sample").agg(list)
    grp.reset_index(inplace=True)

    samples_list = []

    for i in list(grp.itertuples())[:1]:        
        samples_list.append(i.sample)

        all_r1 = " ".join([f"{rawreads_folder}/{x}" for x in i.r1])
        all_r2 = " ".join([f"{rawreads_folder}/{x}" for x in i.r2])

        # check_call(f"mkdir -p {wdir}/{i.sample}", shell=True)

        # check_call(f"cat {all_r1} > {wdir}/{i.sample}/R1.fastq.gz", shell=True)
        # check_call(f"cat {all_r2} > {wdir}/{i.sample}/R2.fastq.gz", shell=True)
    
    return samples_list
