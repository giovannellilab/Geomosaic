
rule run_rmi_rpi_funprofiler:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        db_folder=expand("{rmi_rpi_indexes_extdb_folder}", rmi_rpi_indexes_extdb_folder=config["EXT_DB"]["rmi_rpi_indexes_extdb_folder"])
    output:
        folder=directory("{wdir}/{sample}/metal_indexes_rb/funprof_output"),
        raw_counts="{wdir}/{sample}/metal_indexes_rb/funprof_output/prefetch_out.csv"
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

        funprofiler $seq_file {input.db_folder}/KOs_sketched_scaled_1000.sig.zip {params.user_params} {.folder.folder}/ko_profiles.csv -t {threads} -p {.folder.folder}/prefetch_out.csv

        echo "[+] Removing concatenated reads ..."
        ( cd {output.folder} && rm seq_concat.fastq.gz )
        echo "[SUCCESS] funprofiler job finished for {wildcards.sample} "

        """

rule run_rmi_rpi_indexes:
    input:
        raw_counts= rules.run_funprofiler.output.raw_counts,
        custom_table_metals= expand("{metal_indexes_custom_table}", metal_indexes_custom_table = config["EXT_DB"]["rmi_rpi_indexes"]["metal_index_file_table"])
    output:
        fodler=directory("{wdir}/{sample}/metal_indexes_rb/redox_metabolic-plasticity_indexes")
    run:

        import os
        import pandas as pd
        import math

        def redox_index(acceptors_list: list, donors_list:list):

            num_donors = len(donors_list)
            num_acceptors = len(acceptors_list)
            index = math.log(num_donors) + math.log(num_acceptors)

            return index


        def compute_indexes(raw_ko_file:str, spreadsheet:str):
            
            # RETRIEVING KOS from funprofiler_file
            results = pd.read_csv(raw_ko_file, sep = ',')
            ko_list = results["match_name"].str.split(':').str[1].unique().tolist()
            subset_ = results[["intersect_bp", "match_name"]]
            n_kos = len(ko_list)

            biogeochem_table = pd.read_csv(spreadsheet,sep = ',')
            # 1. Filter Sample KOs in our master table
            detected_mask = master_table['KO'].isin(unique_ko_list)

            filtered_df = master_table[detected_mask]
            # RSTRIP the columns, white spaces !!!!!!!!
            # 2. Split into UNIQUE Donors (D) and Acceptors (A)
            donors_df = filtered_df[filtered_df['energyRole'] == 'D']
            acceptors_df = filtered_df[filtered_df['energyRole'] == 'A']

             # 3. Select DOnors and Acceptors (remove the DROPNA ? )
            unique_donors = donors_df[donors_df['KO'].isin(unique_ko_list)] \ 
            ['biogeoSubstrate'].dropna().unique().tolist() 
            unique_acceptors = acceptors_df[acceptors_df['KO'].isin(unique_ko_list)] \
            ['biogeoSubstrate'].dropna().unique().tolist()

            # 4. Select Donors / Acceptors
            donors = set(donors_df['KO'])
            acceptors = set(acceptors_df['KO'])
            # 5. Select Metal DOnors / acceptors
            metal_donors = donors_df['Metal'].dropna()
            metal_acceptrs = acceptors_df['Metal'].dropna()

            dictio = {"acceptors": metal_acceptors, "donors" : metal_donors}
            for name, lista in dictio.items():
                unique = []
                for row in lista:
                    if isinstance(row, str) and row != '//':
                        row = row.strip() 
                        metals = [metal.strip() for metal in row.split(',')]
                        unique.extend(metals)

                name = f'unique_{name}'
                dictio[name] = set(unique)

            m_a = dictio['acceptors']
            m_d = dictio['donors']  

            # COMPUTING INDEXES
            index_ko_pairs = redox_index(acceptors,donors)
            index_metal_pairs = redox_index(m_a,m_d)

            return float(index_ko_pairs), float(index_metal_pairs)

        index_ko_pairs, index_metal_pairs = compute_indexes(input.raw_counts, input.custom_table_metals)


        out_file = os.path.join(str(output),'metal_indexes.tsv')
        data = {'sample':s,'redox-metabolic-index':index_ko_pairs,'redox-plasticty-index':index_metal_pairs}
        dataframe = pd.DataFrame(data)
        
        with open(out_file,"w") as writer:
            rmi = "	".join(["Redox Metabolic Index",index_ko_pairs])
            rpi = "	".join(["Redox Plasticity Index",index_metal_pairs])
            
            writer.write(rmi + "\n")
            writer.write(rpi + "\n")

