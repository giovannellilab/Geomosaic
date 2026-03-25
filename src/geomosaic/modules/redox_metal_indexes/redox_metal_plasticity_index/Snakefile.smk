
rule run_rmi_mpi_funprofiler:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        db_folder=expand("{redox_metal_indexes_extdb_folder}", redox_metal_indexes_extdb_folder=config["EXT_DB"]["redox_metal_plasticity_index"]["database_folder"])
    output:
        raw_counts="{wdir}/{sample}/{redox_metal_plasticity_index_output_folder}/funprof_output/prefetch_out.csv",
        done="{wdir}/{sample}/{redox_metal_plasticity_index_output_folder}/funprof_output/funprofiler.done"
    conda: config["ENVS"]["redox_metal_plasticity_index"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["redox_metal_plasticity_index"])) ) (config["USER_PARAMS"]["redox_metal_plasticity_index"])
    threads: config["threads"]
    shell:
        """
        export RAYON_NUM_THREADS={threads}
        export OMP_NUM_THREADS={threads}

        ulimit -u 4096
        ulimit -n 4096

        outdir=$(dirname {output.raw_counts})
        mkdir -p $outdir

        echo "[+] Concatenating reads for sample: {wildcards.sample}"
        seq_file="$outdir/seq_concat.fastq.gz"

        cat {input.r1} {input.r2} > $seq_file

        funprofiler $seq_file {input.db_folder}/funprofiler_db/KOs_sketched_scaled_1000.sig.zip {params.user_params} $outdir/ko_profiles.csv -t {threads} -p {output.raw_counts}

        echo "[+] Cleaning temporary files"
        rm -f $seq_file
        rm -f $seq_file"_sketch_"*.sig.zip

        touch {output.done}
        """


rule run_redox_metal_indexes:
    input:
        raw_counts= rules.run_rmi_mpi_funprofiler.output.raw_counts,
        custom_table_metals= expand("{table_file}", table_file = config["EXT_DB"]["redox_metal_plasticity_index"]["table_file"])
    output:
        metal_index="{wdir}/{sample}/{redox_metal_plasticity_index_output_folder}/metabolic_index/metal_indexes.tsv",
        metal_index_extended="{wdir}/{sample}/{redox_metal_plasticity_index_output_folder}/metabolic_index/metal_indexes_extended.tsv"
    run:
        import os
        import pandas as pd
        import numpy as np
        from itertools import product

        def redox_metabolic_index(acceptors_list: list, donors_list:list) -> float:
            
            if len(donors_list) == 0 or len(acceptors_list) == 0:
                return 0.0

            return float(round(np.log(len(donors_list)) + np.log(len(acceptors_list)),4))



        def metal_plasticty_index(metal_donors_l: list, metal_acceptor_l: list) -> float:

            if len(metal_donors_l) == 0 or len(metal_acceptor_l) == 0:
                return 0.0
            else:
                unique_pairs = list({tuple(sorted(pair)) for pair in product(metal_donors_l, metal_acceptor_l)})

            return float(round(np.log(len(unique_pairs)),4))



        def substrate_metal_map(df: pd.DataFrame) -> tuple[dict[str, dict], list[str], list[str]]:

            substrate_map = {}
            unique_metals ,unique_substrates = set(), set()
            no_metal = "__no_metal__"

            for _, row in df.iterrows():
                
                substrate = row['biogeoSubstrate']
                metal = row['Metal']
                ko = row['KO']
                unique_substrates.add(substrate)

                if substrate not in substrate_map:
                    substrate_map[substrate] = {"metals": {}}

                if isinstance(metal, str) and metal != '//':
                    metals = [m.strip() for m in metal.split(',')]
                    for m in metals:
                        unique_metals.add(m)
                        if m not in substrate_map[substrate]["metals"]:
                            substrate_map[substrate]["metals"][m] = [ko]
                        else:
                            substrate_map[substrate]["metals"][m].append(ko)

                elif metal == '//':
                    if no_metal not in substrate_map[substrate]["metals"]:
                        substrate_map[substrate]["metals"][no_metal] = [ko]
                    else:
                        substrate_map[substrate]["metals"][no_metal].append(ko)

            return substrate_map, sorted(list(unique_metals)), sorted(list(unique_substrates))


        def parse_results(s, d, index_substrate_pairs, index_metal_pairs, type_s):
            rows = []
            for substrate, data in d.items():
                for metal, kos in data["metals"].items():
                        rows.append({'sample': s, 'rmi' : index_substrate_pairs, 'mpi' : index_metal_pairs, 
                                     'substrate' : substrate, 'metal': np.nan if metal == "__no_metal__" else metal, 
                                     'type' : type_s, "KO" : kos})
            return pd.DataFrame(rows)
    

        funprofiler_raw_counts = str(input.raw_counts)
        sample = wildcards.sample
        biogeochem_table = str(input.custom_table_metals)

        results = pd.read_csv(funprofiler_raw_counts, sep = ',')
        ko_list = results["match_name"].str.split(':').str[1].unique().tolist()
        subset_ = results[["intersect_bp", "match_name"]]

        biogeochem_table = pd.read_csv(biogeochem_table,sep = '\t')
        filtered_df = biogeochem_table[biogeochem_table['KO'].isin(ko_list)]

        donors_df = filtered_df[filtered_df['energyRole'] == 'D']
        acceptors_df = filtered_df[filtered_df['energyRole'] == 'A']

        data_donors, unq_donor_metals, unq_donors_subs = substrate_metal_map(donors_df)
        data_acceptors, unq_acceptor_metals, unq_acceptor_subs = substrate_metal_map(acceptors_df)

        rmi = redox_metabolic_index(unq_donors_subs,unq_acceptor_subs)
        mpi = metal_plasticty_index(unq_donor_metals,unq_acceptor_metals)

        results_donors = parse_results(sample, data_donors, rmi, mpi,type_s= 'donors')
        results_acceptors = parse_results(sample, data_acceptors, rmi, mpi, type_s='acceptors')

        df_ext = pd.concat([results_donors, results_acceptors], ignore_index=True)

        out_file_extended = os.path.join(str(output.metal_index_extended))
        df_ext.to_csv(out_file_extended, sep='\t', index=False)

        out_file_truncated = os.path.join(str(output.metal_index))
        df_trunc = pd.DataFrame({
            'sample': [sample],
            'redox_metabolic_index': [rmi],
            'metal_plasticty_index': [mpi],
            'acceptors_metals': str(unq_acceptor_metals),
            'donors_metal': str(unq_donor_metals),
            'acceptor_substrates': str(unq_acceptor_subs),
            'donor_substrates': str(unq_donors_subs)
        })
        df_trunc.to_csv(out_file_truncated, sep='\t', index=False)