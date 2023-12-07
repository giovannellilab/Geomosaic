
rule recognizer_db:
    output:
        directory(expand("{recognizer_extdb_folder}", recognizer_extdb_folder = config["EXT_DB"]["recognizer"]))
    conda: config["ENVS"]["recognizer"]
    message: "GEOMOSAIC MSG: Starting to setup the database for reCOGnizer"
    log: "{recognizer_extdb_folder}/log.out"
    shell:
        """
        mkdir -p {output}/null_results
        (cd {output} & recognizer --resources-directory {output} --download-resources --output {output}/null_results >> {log} 2>&1 ) || true
        """
