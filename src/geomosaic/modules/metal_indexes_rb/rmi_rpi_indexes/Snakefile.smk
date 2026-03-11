
rule run_rmi_rpi_funprofiler:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        db_folder=expand("{rmi_rpi_indexes_extdb_folder}", rmi_rpi_indexes_extdb_folder=config["EXT_DB"]["rmi_rpi_indexes"]["database_folder"])
    output:
        folder = directory("{wdir}/{sample}/{rmi_rpi_output_folder}/funprof_output"),
        raw_counts="{wdir}/{sample}/{rmi_rpi_output_folder}/funprof_output/prefetch_out.csv"
    conda: config["ENVS"]["rmi_rpi_indexes"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["rmi_rpi_indexes"])) ) (config["USER_PARAMS"]["rmi_rpi_indexes"])
    threads: config["threads"]
    shell:
        """
        # This ensures parallel libraries (like Rayon and OpenMP) respect the allocated threads.
        
        export RAYON_NUM_THREADS={threads}
        export OMP_NUM_THREADS={threads}

        # Increase OS limits for processes/files to prevent I/O errors

        ulimit -u 4096
        ulimit -n 4096
        # --------------------------------------------------------------------------------------- #

        mkdir -p {output.folder}

        echo "[+] Concatenating reads for sample: {wildcards.sample} "
        seq_file="{output.folder}/seq_concat.fastq.gz"

        cat {input.r1} {input.r2} > $seq_file
        echo "[+] Reads successfully concatenated into $seq_file "

        funprofiler $seq_file {input.db_folder}/funprofiler_db/KOs_sketched_scaled_1000.sig.zip {params.user_params} {output.folder}/ko_profiles.csv -t {threads} -p {output.folder}/prefetch_out.csv

        echo "[+] Removing concatenated reads ..."
        ( cd {output.folder} && rm seq_concat.fastq.gz )
        echo "[+] Removing sketched metagenome ..."
        ( cd {output.folder} && rm -f seq_concat.fastq.gz_sketch_*.sig.zip)
        echo "[SUCCESS] funprofiler job finished for {wildcards.sample} "

        """


rule run_rmi_rpi_indexes:
    input:
        raw_counts= rules.run_rmi_rpi_funprofiler.output.raw_counts,
        custom_table_metals= expand("{table_file}", table_file = config["EXT_DB"]["rmi_rpi_indexes"]["table_file"])
    output:
        metal_index="{wdir}/{sample}/{rmi_rpi_output_folder}/redox_metabolic_plasticity_indexes/metal_indexes.tsv",
        metal_index_extended="{wdir}/{sample}/{rmi_rpi_output_folder}/redox_metabolic_plasticity_indexes/metal_indexes_extended.tsv"
    run:
        import os
        import pandas as pd
        import math



        def redox_index(acceptors_list: list, donors_list:list) -> float:
            num_donors = len(donors_list)
            num_acceptors = len(acceptors_list)
            if num_donors == 0 or num_acceptors == 0:
                return 0.0
            return float(round(math.log(num_donors) + math.log(num_acceptors),4))


        def substrate_metal_map(df: pd.DataFrame) -> tuple[dict[str, set], list[str]]:
            substrate_map = {}
            unique_metals = set()

            for _, row in df.iterrows():
                substrate = row['biogeoSubstrate']
                metal = row['Metal']
                if pd.isna(substrate):
                    continue
                if substrate not in substrate_map:
                    substrate_map[substrate] = set()
                if isinstance(metal, str) and metal != '//':
                    metals = [m.strip() for m in metal.split(',')]
                    substrate_map[substrate].update(metals)

            for sub, metals in substrate_map.items():
                unique_metals.update(metals)

            return substrate_map, list(unique_metals)

        def parse_results(s, d, index_substrate_pairs, index_metal_pairs, type_s):
            rows = []
            for substrate, metals in d.items():
                if metals:  # skip empty sets like 'Water'
                    for metal in metals:
                        rows.append({'sample': s, 'rmi' : index_substrate_pairs, 'rpi' : index_metal_pairs, \
                        'substrate' : substrate, 'metal': metal, 'type' : type_s})

            return pd.DataFrame(rows)
    

        results = pd.read_csv(str(input.raw_counts), sep = ',')
        ko_list = results["match_name"].str.split(':').str[1].unique().tolist()
        subset_ = results[["intersect_bp", "match_name"]]

        # 1. Filter Sample KOs in our master table
        biogeochem_table = pd.read_csv(str(input.custom_table_metals),sep = '\t')
        filtered_df = biogeochem_table[biogeochem_table['KO'].isin(ko_list)]

        # 2. Split into UNIQUE Donors (D) and Acceptors (A)
        donors_df = filtered_df[filtered_df['energyRole'] == 'D']
        acceptors_df = filtered_df[filtered_df['energyRole'] == 'A']

        # 3. Select Donors / Acceptors
        donors = set(donors_df['KO'])
        acceptors = set(acceptors_df['KO'])

       # 3.2 Select Donors and Acceptors
        unique_donors = donors_df['biogeoSubstrate'].dropna().unique().tolist()
        unique_acceptors = acceptors_df['biogeoSubstrate'].dropna().unique().tolist()

        donors_subs, unique_donor_metals = substrate_metal_map(donors_df)
        acceptors_subs , unique_acceptor_metals = substrate_metal_map(acceptors_df)

        index_substrate_pairs = redox_index(unique_acceptors,unique_donors)
        index_metal_pairs = redox_index(unique_acceptor_metals,unique_donor_metals)

        results_donors = parse_results(wildcards.sample,donors_subs, index_metal_pairs, index_substrate_pairs,type_s='donors')
        results_acceptors = parse_results(wildcards.sample,acceptors_subs, index_metal_pairs, index_metal_pairs, type_s='acceptors')

        df_ext = pd.concat([results_donors, results_acceptors], ignore_index=True)

        out_file_extended = os.path.join(str(output.metal_index_extended))
        df_ext.to_csv(out_file_extended, sep='\t', index=False)

        out_file_truncated = os.path.join(str(output.metal_index))
        df_trunc = pd.DataFrame({
            'sample': [wildcards.sample],
            'redox-metabolic-index': [index_substrate_pairs],
            'redox-plasticty-index': [index_metal_pairs],
            'acceptors_metals': str(unique_acceptor_metals),
            'donors_metal': str(unique_donor_metals),
            'acceptor_substrates': str(unique_acceptors),
            'donor_substrates': str(donors_subs)
        })
        df_trunc.to_csv(out_file_truncated, sep='\t', index=False)