
checkpoint run_mags_kofam_scan_redox_metal_plasticity_index:
    input:
        mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}/{mag}/orf_predicted.faa", mags_orf_prediction=config["MODULES"]["mags_orf_prediction"], allow_missing=True),
        db_folder=expand("{kofam_scan_extdb_folder}", kofam_scan_extdb_folder=config["EXT_DB"]["mags_kofam_scan_redox_metal_plasticity_index"]["database_folder"])
    output:
        kofamscan_result="{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/{mag}/result.txt",
        tmp_dir=temp(directory("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/{mag}/temp_geomosaic_dir"))
    conda: config["ENVS"]["mags_kofam_scan_redox_metal_plasticity_index"]
    params:
        user_params= ( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["mags_kofam_scan_redox_metal_plasticity_index"])) ) (config["USER_PARAMS"]["mags_kofam_scan_redox_metal_plasticity_index"]),
        user_kofam_profiles = (lambda x: yaml.safe_load(open(x, "r"))["mags_kofam_scan_profiles"]) (config["USER_PARAMS"]["mags_kofam_scan_redox_metal_plasticity_index"]) 
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

rule gather_mags_kofam_scan_redox_metal_plasticity_index_inputs:
    input: get_kofamscan_inputs("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/{mag}/result.txt")
    output: touch("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/gather_OK.txt")
    threads: 1


rule format_mags_kofam_scan_redox_metal_plasticity_index_output:
    input:
        result=rules.run_mags_kofam_scan_redox_metal_plasticity_index.output.kofamscan_result
    output:
        formatted="{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/{mag}/kofam_formatted.csv"
    run:
        import pandas as pd

        def parse_kofam_result(path: str) -> list:
            kos = []
            with open(path) as fh:
                for line in fh:
                    if not line.strip() or line.startswith('#') or not line.startswith('*'):
                        continue
                    fields = line.split()
                    if len(fields) >= 3:
                        kos.append(f"gene:{fields[2]}")
            return kos

        ko_list = parse_kofam_result(str(input.result))

        df = (
            pd.Series(ko_list)
            .value_counts()
            .reset_index(name="intersect_bp")
            .rename(columns={"index": "match_name"})
            [["intersect_bp", "match_name"]]
        )

        df.to_csv(str(output.formatted), index=False)


rule run_mags_redox_metal_plasticity_index:
    input:
        raw_counts=rules.format_mags_kofam_scan_redox_metal_plasticity_index_output.output.formatted,
        custom_table_metals=expand("{table_file}", table_file=config["EXT_DB"]["mags_kofam_scan_redox_metal_plasticity_index"]["table_file"])
    output:
        metal_index="{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/{mag}/metabolic_index/redox_metal_indexes.tsv",
        metal_index_extended="{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/{mag}/metabolic_index/redox_metal_indexes_extended.tsv"
    run:
        import os
        import pandas as pd

        from geomosaic.custom_tools.redox_metal_plasticity_index_custom import (
            redox_metabolic_index,
            metal_plasticity_index,
            substrate_metal_map,
            parse_results
        )

        raw_counts_file = str(input.raw_counts)
        sample_mag = f"{wildcards.sample}_{wildcards.mag}"
        biogeochem_table = str(input.custom_table_metals)

        results = pd.read_csv(raw_counts_file, sep=',')
        ko_list = results["match_name"].str.split(':').str[1].unique().tolist()

        biogeochem_table = pd.read_csv(biogeochem_table, sep='\t')
        filtered_df = biogeochem_table[biogeochem_table['KO'].isin(ko_list)]

        donors_df = filtered_df[filtered_df['energyRole'] == 'D']
        acceptors_df = filtered_df[filtered_df['energyRole'] == 'A']

        data_donors, unq_donor_metals, unq_donors_subs = substrate_metal_map(donors_df)
        data_acceptors, unq_acceptor_metals, unq_acceptor_subs = substrate_metal_map(acceptors_df)

        rmi = redox_metabolic_index(unq_donors_subs, unq_acceptor_subs)
        mpi = metal_plasticity_index(unq_donor_metals, unq_acceptor_metals)

        results_donors = parse_results(sample_mag, data_donors, rmi, mpi, type_s='donors')
        results_acceptors = parse_results(sample_mag, data_acceptors, rmi, mpi, type_s='acceptors')

        df_ext = pd.concat([results_donors, results_acceptors], ignore_index=True)
        df_ext["KO"] = df_ext.apply(lambda x: ";".join(x["KO"]), axis=1)
        df_ext.to_csv(str(output.metal_index_extended), sep='\t', index=False)

        df_trunc = pd.DataFrame({
            'sample': [sample_mag],
            'redox_metabolic_index': [float(rmi)],
            'metal_plasticity_index': [float(mpi)],
            'acceptors_metals': ";".join(unq_acceptor_metals),
            'donors_metal': ";".join(unq_donor_metals),
            'acceptor_substrates': ";".join(unq_acceptor_subs),
            'donor_substrates': ";".join(unq_donors_subs)
        })
        df_trunc.to_csv(str(output.metal_index), sep='\t', index=False)


rule gather_mags_redox_metal_plasticity_index:
    input:
        collected=get_kofamscan_inputs("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/{mag}/metabolic_index/redox_metal_indexes.tsv"),
        mags_tsv=expand("{wdir}/{sample}/{mags_retrieval}/MAGs.tsv", mags_retrieval=config["MODULES"]["mags_retrieval"], allow_missing=True)
    output: touch("{wdir}/{sample}/mags_kofam_scan_redox_metal_plasticity_index/gather_redox_metal_index_OK.txt")
    threads: 1