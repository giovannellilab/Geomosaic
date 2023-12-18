
rule mifaser_db:
    params: 
        db_version="GS-21-all",
        diamond_file="https://bitbucket.org/bromberglab/mifaser/raw/bbd1ca1d093d8a26060ee83daf2d7f3f5e88bfd0/mifaser/database/GS-21-all/database.dmnd",
        sequence_file="https://bitbucket.org/bromberglab/mifaser/raw/bbd1ca1d093d8a26060ee83daf2d7f3f5e88bfd0/mifaser/database/GS-21-all/sequences.fasta",
        annotation_file="https://bitbucket.org/bromberglab/mifaser/raw/bbd1ca1d093d8a26060ee83daf2d7f3f5e88bfd0/mifaser/database/GS-21-all/ec_annotation.tsv",
        mapping_file="https://bitbucket.org/bromberglab/mifaser/raw/bbd1ca1d093d8a26060ee83daf2d7f3f5e88bfd0/mifaser/database/GS-21-all/ec_mapping.tsv",
    output:
        directory(expand("{mifaser_extdb_folder}", mifaser_extdb_folder=config["EXT_DB"]["mifaser"]))
    message: "GEOMOSAIC MSG: Starting to setup the database for mi-faser"
    threads: 1
    shell:
        """
        mkdir -p {output}/{params.db_version}
        (cd {output}/{params.db_version} && wget --quiet {params.diamond_file} && wget --quiet {params.sequence_file} && wget --quiet {params.annotation_file} && wget --quiet {params.mapping_file})
        """

