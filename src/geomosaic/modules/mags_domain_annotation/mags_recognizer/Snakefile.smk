
rule run_recognizer_db:
    output:
        directory("{wdir}/reCOGnizer_DB")
    run:
        shell("mkdir -p {output}")
        shell("(cd {output} & recognizer --resources-directory {output} --download-resources)")


rule run_mags_recognizer:
    input:
        mags_orf=expand("{wdir}/{sample}/{mags_orf_prediction}", mags_orf_prediction=config["mags_orf_prediction"], allow_missing=True),
        recognizer_db={rules.run_recognizer_db.output}
    output:
        directory("{wdir}/{sample}/mags_recognizer")
    params:
        skip_download="--skip-downloaded"
    threads: 5
    run:
        mags_list = []
        mags_list_file = os.path.join(str(input.mags_orf), "mags_list.txt")
        
        with open(mags_list_file) as fd:
            for line in fd:
                mags_list.append(line.rstrip("\n"))
    
        for mag in mags_list:
            orf_mag_file=os.path.join(str(input.mags_orf), mag, "orf_predicted.faa")
            mag_output=os.path.join(str(output), mag)
            shell("mkdir -p {mag_output}")
            shell("cd {mag_output} & recognizer \
                    --file {orf_mag_file} \
                    --output {mag_output} \
                    --resources-directory {input.recognizer_db} \
                    {params.skip_download} \
                    --threads {threads}")
