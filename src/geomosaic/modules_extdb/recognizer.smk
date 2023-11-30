
rule run_recognizer_db:
    output:
        directory("{wdir}/reCOGnizer_DB")
    params:
        download_resource="--download-resources"
    run:
        shell("mkdir -p {output}/null_results")
        shell("(cd {output} & recognizer --resources-directory {output} {params.download_resource} --output {output}/null_results)")
