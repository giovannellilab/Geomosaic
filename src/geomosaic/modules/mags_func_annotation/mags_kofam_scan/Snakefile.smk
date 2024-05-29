
checkpoint run_mags_kofam_scan:
    input:
        mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/orf_predicted.faa", mags_orf_prediction=config["MODULES"]["mags_orf_prediction"], allow_missing=True),
        db_folder=expand("{kofam_scan_extdb_folder}", kofam_scan_extdb_folder=config["EXT_DB"]["mags_kofam_scan"])
    output:
        kofamscan_result="{wdir}/{sample}/mags_kofam_scan/{mag}/result.txt",
        tmp_dir=temp(directory("{wdir}/{sample}/mags_kofam_scan/{mag}/temp_geomosaic_dir"))
    conda: config["ENVS"]["mags_kofam_scan"]
    params:
        user_params= ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags_kofam_scan"])) ) (config["USER_PARAMS"]["mags_kofam_scan"]),
        user_kofam_profiles = (lambda x: yaml.safe_load(open(x, "r"))["mags_kofam_scan_profiles"]) (config["USER_PARAMS"]["mags_kofam_scan"]) 
    threads: config["threads"]
    shell:
        """
        kofamscan_folder=$(dirname {output.kofamscan_result})

        mkdir -p $kofamscan_folder

        exec_annotation \
            {params.user_params} \
            --profile {input.db_folder}/{params.user_kofam_profiles} \
            --ko-list {input.db_folder}/ko_list \
            --cpu {threads} \
            --tmp-dir {output.tmp_dir} \
            -o {output.kofamscan_result} \
            {input.mags_orf}
        """

def get_kofamscan_inputs(f_string): 
    def _f(wildcards):
        import pandas as pd

        mags_file = "{wdir}/{sample}/MAGs.tsv"
        df_mags = pd.read_csv(mags_file.format(**wildcards), sep="\t")
        
        _temp = []
        for m in df_mags.MAGs:
            _temp.append(f_string.format(mag=m, **wildcards) )

        return _temp
    return _f

rule gather_mags_kofam_scan_inputs:
    input: get_kofamscan_inputs("{wdir}/{sample}/mags_kofam_scan/{mag}/result.txt")
    output: touch("{wdir}/{sample}/mags_kofam_scan/gather_OK.txt")
    threads: 1

