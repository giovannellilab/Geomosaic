
rule run_rmi_mpi_kofam_scan:
    input:
        orf_predicted=expand("{wdir}/{sample}/{orf_prediction}/orf_predicted.faa", orf_prediction=config["MODULES"]["orf_prediction"], allow_missing=True),
        db_folder=expand("{kofam_scan_redox_metal_plasticity_index_extdb_folder}", kofam_scan_redox_metal_plasticity_index_extdb_folder=config["EXT_DB"]["kofam_scan_redox_metal_plasticity_index"]["database_folder"])
    output:
        result="{wdir}/{sample}/{kofam_scan_redox_metal_plasticity_index_output_folder}/kofam_scan_output/result.txt",
        tmp_dir=temp(directory("{wdir}/{sample}/{kofam_scan_redox_metal_plasticity_index_output_folder}/kofam_scan_output/temp_geomosaic_dir")),
        done="{wdir}/{sample}/{kofam_scan_redox_metal_plasticity_index_output_folder}/kofam_scan_output/kofam_scan.done"
    conda: config["ENVS"]["kofam_scan_redox_metal_plasticity_index"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["kofam_scan_redox_metal_plasticity_index"])) ) (config["USER_PARAMS"]["kofam_scan_redox_metal_plasticity_index"]),
        user_kofam_profiles=(lambda x: yaml.safe_load(open(x, "r"))["kofam_scan_profiles"]) (config["USER_PARAMS"]["kofam_scan_redox_metal_plasticity_index"])
    threads: config["threads"]
    shell:
        """
        outdir=$(dirname {output.result})
        mkdir -p $outdir
        mkdir -p {output.tmp_dir}

        echo "[+] Running kofam_scan (exec_annotation) for sample: {wildcards.sample}"

        exec_annotation \
            {params.user_params} \
            --profile {input.db_folder}/{params.user_kofam_profiles} \
            --ko-list {input.db_folder}/ko_list \
            --cpu {threads} \
            --tmp-dir {output.tmp_dir} \
            -o {output.result} \
            {input.orf_predicted}

        touch {output.done}
        """


rule format_kofam_scan_output:
    input:
        result=rules.run_rmi_mpi_kofam_scan.output.result
    output:
        formatted="{wdir}/{sample}/{kofam_scan_redox_metal_plasticity_index_output_folder}/kofam_scan_output/kofam_formatted.csv"
    params:
        user_params_file=config["USER_PARAMS"]["kofam_scan_redox_metal_plasticity_index"]
    run:
        import pandas as pd

        raw_threshold = yaml.safe_load(open(str(params.user_params_file), "r")).get("kofam_evalue_threshold")
        evalue_threshold = float(raw_threshold) if raw_threshold not in (None, "") else None

        def parse_kofam_result(path: str, evalue_threshold=None) -> list:
            kos = []
            with open(path) as fh:
                for line in fh:
                    if not line.strip() or line.startswith('#') or not line.startswith('*'):
                        continue
                    fields = line.split()
                    if len(fields) < 6:
                        continue
                    if evalue_threshold is not None:
                        try:
                            evalue = float(fields[5])
                        except ValueError:
                            continue
                        if evalue > evalue_threshold:
                            continue
                    kos.append(f"gene:{fields[2]}")
            return kos

        ko_list = parse_kofam_result(str(input.result), evalue_threshold=evalue_threshold)

        df = (
            pd.Series(ko_list)
            .value_counts()
            .reset_index(name="intersect_bp")
            .rename(columns={"index": "match_name"})
            [["intersect_bp", "match_name"]]
        )

        df.to_csv(str(output.formatted), index=False)


rule run_kofam_scan_redox_metal_plasticity_index:
    input:
        raw_counts=rules.format_kofam_scan_output.output.formatted,
        custom_table_metals=expand("{table_file}", table_file=config["EXT_DB"]["kofam_scan_redox_metal_plasticity_index"]["table_file"])
    output:
        metal_index="{wdir}/{sample}/{kofam_scan_redox_metal_plasticity_index_output_folder}/metabolic_index/redox_metal_indexes.tsv",
        metal_index_extended="{wdir}/{sample}/{kofam_scan_redox_metal_plasticity_index_output_folder}/metabolic_index/redox_metal_indexes_extended.tsv"
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
        sample = wildcards.sample
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

        results_donors = parse_results(sample, data_donors, rmi, mpi, type_s='donors')
        results_acceptors = parse_results(sample, data_acceptors, rmi, mpi, type_s='acceptors')

        df_ext = pd.concat([results_donors, results_acceptors], ignore_index=True)

        out_file_extended = os.path.join(str(output.metal_index_extended))
        df_ext["KO"] = df_ext.apply(lambda x: ";".join(x["KO"]), axis=1)
        df_ext.to_csv(out_file_extended, sep='\t', index=False)

        out_file_truncated = os.path.join(str(output.metal_index))
        df_trunc = pd.DataFrame({
            'sample': [sample],
            'redox_metabolic_index': [float(rmi)],
            'metal_plasticity_index': [float(mpi)],
            'acceptors_metals': ";".join(unq_acceptor_metals),
            'donors_metal': ";".join(unq_donor_metals),
            'acceptor_substrates': ";".join(unq_acceptor_subs),
            'donor_substrates': ";".join(unq_donors_subs)
        })
        df_trunc.to_csv(out_file_truncated, sep='\t', index=False)