
rule run_funprofiler:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        db_folder=expand("{funprofiler_extdb_folder}", funprofiler_extdb_folder=config["EXT_DB"]["funprofiler"]),
    output:
        directory("{wdir}/{sample}")
    conda: config["ENVS"]["funprofiler"]
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["funprofiler"])) ) (config["USER_PARAMS"]["funprofiler"]),
    threads: config["threads"]
    shell:
        """
        # This ensures parallel libraries (like Rayon and OpenMP) respect the allocated threads.
        
        shell(export RAYON_NUM_THREADS={threads}
        export OMP_NUM_THREADS={threads}

        # Increase OS limits for processes/files to prevent I/O errors

        ulimit -u 4096
        ulimit -n 4096
        # --------------------------------------------------------------------------------------- #

        mkdir -p {output}

        echo "[+] Concatenating reads for sample: {wildcards.sample} "
        seq_file="{output}/seq_concat.fastq.gz"

        cat {input.r1} {input.r2} > $seq_file
        echo "[+] Reads successfully concatenated into $seq_file " 

        funprofiler $seq_file {input.db_folder}/KOs_sketched_scaled_1000.sig.zip {params.user_params} {output}/ko_profiles.csv -t {threads} -p {output}/prefetch_out.csv

        echo "[+] Removing concatenated reads ..."
        ( cd {output} && rm seq_concat.fastq.gz )
        echo "[SUCCESS] funprofiler job finished for {wildcards.sample} "

        raw_table="{output}/prefetch_out.csv"

        """

rule run_mi_rpi_funprofile_based:
    input:
        raw_counts= rules.run_funprofiler.output
        custom_table_metals= expand("{funprofiler_biogeochem_table}", funprofiler_biogeochem_table = config["EXT_DB"]["metal_indexes"])
    output:
        out_file = directory("{wdir}/{sample}/mi_rpi_funprofiler_based/metal_indexes.tsv")
    run:

        import OS
        import pandas as pd
        import math 

        def validate(file_path):
            required = {{"energy_role", "Metal", "KO", "biogeoSubstrate"}}
            try:
                with open(file_path, 'r') as f:
                    reader = csv.DictReader(f, delimiter='\\t')
                    if not reader.fieldnames:
                        print("Validation Error: File is empty")
                        sys.exit(1)

                    actual = set(reader.fieldnames)
                    missing = required - actual
                    if missing:
                        print(f"Validation Error: Missing columns {{missing}}")
                        sys.exit(1)
                    print("Validation Passed!")
            except Exception as e:
                print(f"Validation Error: {{e}}")
                sys.exit(1)


        def redox_index(acceptors_list: list, donors_list:list):

            num_donors = len(donors_list)
            num_acceptors = len(acceptors_list)

            index = math.log(num_donors) + math.log(num_acceptors)

            return index

        validate("{output}/prefetch_out.csv")



        if os.path.exists(table):
            results = pd.read_csv(table, sep = ',')

            ko_list = results["match_name"].str.split(':').str[1].unique().tolist()
            subset_ = results[["intersect_bp", "match_name"]]
            n_kos = len(ko_list)

        biogeochem_table = ""
        master_table = pd.read_csv(spreadsheet,sep = ',')
        # 1. Filter Sample KOs in our master table
        detected_mask = master_table['KO'].isin(unique_ko_list)
        filtered_df = master_table[detected_mask]

        # 2. Split into UNIQUE Donors (D) and Acceptors (A)
        donors_df = filtered_df[filtered_df['energyRole'] == 'D']
        acceptors_df = filtered_df[filtered_df['energyRole'] == 'A']
        # 3. Select cofactors
        donors = set(donors_df['KO'])
        acceptors = set(acceptors_df['KO'])

        metal_donors = donors_df['Metal'].dropna()
        metal_acceptrs = acceptors_df['Metal'].dropna()

        m_a = set(metal_acceptrs)
        m_d = set(metal_donors)

        index_ko_pairs = redox_index(acceptors,donors)
        index_metal_pairs = redox_index(m_a,m_d)

        with open(out_file,"w") as writer:
            rmi = "	".join(["Redox Metabolic Index",index_ko_pairs])
            rpi = "	".join(["Redox Plasticity Index",index_metal_pairs])
            
            writer.write(rmi + "\n")
            writer.write(rpi + "\n")

