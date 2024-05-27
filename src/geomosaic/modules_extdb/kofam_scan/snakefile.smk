
rule kofam_scan_db:
    params: 
        kolist="https://www.genome.jp/ftp/db/kofam/ko_list.gz",
        kolist_file="ko_list.gz",
        profiles="https://www.genome.jp/ftp/db/kofam/profiles.tar.gz",
        profiles_file="profiles.tar.gz"
    output:
        directory(expand("{kofam_scan_extdb_folder}", kofam_scan_extdb_folder=config["EXT_DB"]["kofam_scan"]))
    message: "GEOMOSAIC MSG: Starting to setup the database for KOfam Scan"
    threads: 1
    shell:
        """
        mkdir -p {output}/prokaryotes 
        mkdir -p {output}/eukaryotes
        mkdir -p {output}/both

        curl --silent --output {output}/{params.kolist_file} {params.kolist}
        curl --silent --output {output}/{params.profiles_file} {params.profiles}

        ( cd {output} && gzip -d {params.kolist_file} )
        ( cd {output} && tar -x -f {params.profiles_file} )

        echo "Copying Prokaryotes profiles..."
        while IFS= read -r hmm
        do
            cp {output}/profiles/$hmm {output}/prokaryotes/
        done < {output}/profiles/prokaryote.hal

        echo "Copying Eukaryotes profiles..."
        while IFS= read -r hmm
        do
            cp {output}/profiles/$hmm {output}/eukaryotes/
        done < {output}/profiles/eukaryote.hal

        echo "Copying both Prokaryotes and Eukaryotes profiles..."
        for hmm in {output}/profiles/*.hmm
        do
            cp $hmm {output}/both/
        done;

        """
