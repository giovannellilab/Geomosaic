
rule kofam_scan_redox_metal_plasticty_index_custom_db:
    params:
        user_table = config["CUSTOM_DB"]["kofam_scan_redox_metal_plasticty_index"]["user_metal_table"],
        kolist="https://www.genome.jp/ftp/db/kofam/ko_list.gz",
        kolist_file="ko_list.gz",
        profiles="https://www.genome.jp/ftp/db/kofam/profiles.tar.gz",
        profiles_file="profiles.tar.gz"
    output:
        kofam_scan_redox_metal_plasticty_index = directory(expand("{kofam_scan_redox_metal_plasticty_index_extdb_folder}", kofam_scan_redox_metal_plasticty_index_extdb_folder=config["EXT_DB"]["kofam_scan_redox_metal_plasticty_index"]["database_folder"])),
        table_file = expand("{table_file}", table_file = config["EXT_DB"]["kofam_scan_redox_metal_plasticty_index"]["table_file"])
    conda: config["ENVS_EXTDB"]["kofam_scan_redox_metal_plasticty_index"]
    message: "GEOMOSAIC MSG: Starting to setup the custom database for KOfam Scan-based RM-RP Indexes"
    threads: 1
    shell:
        """
        mkdir -p {output.kofam_scan_redox_metal_plasticty_index}/prokaryotes
        mkdir -p {output.kofam_scan_redox_metal_plasticty_index}/eukaryotes
        mkdir -p {output.kofam_scan_redox_metal_plasticty_index}/both

        cp {params.user_table} {output.table_file}

        curl --silent --output {output.kofam_scan_redox_metal_plasticty_index}/{params.kolist_file} {params.kolist}
        curl --silent --output {output.kofam_scan_redox_metal_plasticty_index}/{params.profiles_file} {params.profiles}

        ( cd {output.kofam_scan_redox_metal_plasticty_index} && gzip -d {params.kolist_file} )
        ( cd {output.kofam_scan_redox_metal_plasticty_index} && tar -x -f {params.profiles_file} )

        echo "Copying Prokaryotes profiles..."
        while IFS= read -r hmm
        do
            cp {output.kofam_scan_redox_metal_plasticty_index}/profiles/$hmm {output.kofam_scan_redox_metal_plasticty_index}/prokaryotes/
        done < {output.kofam_scan_redox_metal_plasticty_index}/profiles/prokaryote.hal

        echo "Copying Eukaryotes profiles..."
        while IFS= read -r hmm
        do
            cp {output.kofam_scan_redox_metal_plasticty_index}/profiles/$hmm {output.kofam_scan_redox_metal_plasticty_index}/eukaryotes/
        done < {output.kofam_scan_redox_metal_plasticty_index}/profiles/eukaryote.hal

        echo "Copying both Prokaryotes and Eukaryotes profiles..."
        for hmm in {output.kofam_scan_redox_metal_plasticty_index}/profiles/*.hmm
        do
            cp $hmm {output.kofam_scan_redox_metal_plasticty_index}/both/
        done;
        """