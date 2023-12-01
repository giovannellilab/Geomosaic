
rule recognizer_db:
    output:
        directory(expand("{recognizer_extdb_folder}", recognizer_extdb_folder = config["EXT_DB"]["recognizer"]))
    params:
        download_resource="--download-resources"
    run:
        shell("mkdir -p {output}/null_results")
        shell("(cd {output} & recognizer --resources-directory {output} {params.download_resource} --output {output}/null_results)")
