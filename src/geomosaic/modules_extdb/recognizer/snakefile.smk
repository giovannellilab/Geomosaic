
rule recognizer_db:
    output:
        directory(expand("{recognizer_extdb_folder}", recognizer_extdb_folder = config["EXT_DB"]["recognizer"]))
    conda: config["ENVS"]["recognizer"]
    message: "GEOMOSAIC MSG: Starting to setup the database for reCOGnizer"
    shell:
        """
        mkdir -p {output}/null_results

        touch {output}/log.out

        (cd {output} & recognizer --resources-directory {output} --output {output}/null_results >> {output}/log.out 2>&1 ) || true
        """
