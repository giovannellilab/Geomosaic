
rule mags_kofam_scan_redox_metal_plasticity_index_custom_db:
    params:
        user_table = config["CUSTOM_DB"]["mags_kofam_scan_redox_metal_plasticity_index"]["user_metal_table"],
        kolist="https://www.genome.jp/ftp/db/kofam/ko_list.gz",
        kolist_file="ko_list.gz",
        profiles="https://www.genome.jp/ftp/db/kofam/profiles.tar.gz",
        profiles_file="profiles.tar.gz"
    output:
        mags_kofam_scan_redox_metal_plasticity_index = directory(expand("{mags_kofam_scan_redox_metal_plasticity_index_extdb_folder}", mags_kofam_scan_redox_metal_plasticity_index_extdb_folder=config["EXT_DB"]["mags_kofam_scan_redox_metal_plasticity_index"]["database_folder"])),
        table_file = expand("{table_file}", table_file = config["EXT_DB"]["mags_kofam_scan_redox_metal_plasticity_index"]["table_file"])
    conda: config["ENVS_EXTDB"]["mags_kofam_scan_redox_metal_plasticity_index"]
    message: "GEOMOSAIC MSG: Starting to setup the custom database for KOfam Scan-based RM-RP Indexes"
    threads: 1
    shell:
        """
        mkdir -p {output.mags_kofam_scan_redox_metal_plasticity_index}/prokaryotes
        mkdir -p {output.mags_kofam_scan_redox_metal_plasticity_index}/eukaryotes
        mkdir -p {output.mags_kofam_scan_redox_metal_plasticity_index}/both

        cp {params.user_table} {output.table_file}

        curl --silent --output {output.mags_kofam_scan_redox_metal_plasticity_index}/{params.kolist_file} {params.kolist}
        curl --silent --output {output.mags_kofam_scan_redox_metal_plasticity_index}/{params.profiles_file} {params.profiles}

        ( cd {output.mags_kofam_scan_redox_metal_plasticity_index} && gzip -d {params.kolist_file} )
        ( cd {output.mags_kofam_scan_redox_metal_plasticity_index} && tar -x -f {params.profiles_file} )

        echo "Copying Prokaryotes profiles..."
        while IFS= read -r hmm
        do
            cp {output.mags_kofam_scan_redox_metal_plasticity_index}/profiles/$hmm {output.mags_kofam_scan_redox_metal_plasticity_index}/prokaryotes/
        done < {output.mags_kofam_scan_redox_metal_plasticity_index}/profiles/prokaryote.hal

        echo "Copying Eukaryotes profiles..."
        while IFS= read -r hmm
        do
            cp {output.mags_kofam_scan_redox_metal_plasticity_index}/profiles/$hmm {output.mags_kofam_scan_redox_metal_plasticity_index}/eukaryotes/
        done < {output.mags_kofam_scan_redox_metal_plasticity_index}/profiles/eukaryote.hal

        echo "Copying both Prokaryotes and Eukaryotes profiles..."
        for hmm in {output.mags_kofam_scan_redox_metal_plasticity_index}/profiles/*.hmm
        do
            cp $hmm {output.mags_kofam_scan_redox_metal_plasticity_index}/both/
        done;
        """