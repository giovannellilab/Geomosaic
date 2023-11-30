
rule db_kaiju:
    params: 
        db="https://kaiju.binf.ku.dk/database/kaiju_db_viruses_2022-03-29.tgz",
        filename="kaiju_db.tgz"
    output:
        directory("{wdir}/kaijudb")
    shell:
        """
        mkdir -p {output}
        curl --output {output}/{params.filename} {params.db}
        (cd {output} && tar --extract --file={params.filename} && mv kaiju_db_*.fmi kaiju_db.fmi && rm {params.filename})
        """

rule run_kaiju:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        kaijudb={rules.db_kaiju.output}
    output:
        fout="{wdir}/{sample}/kaiju/kaiju.out"
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["kaiju"])) ) (config["USER_PARAMS"]["kaiju"])
    threads: 5
    conda: config["ENVS"]["kaiju"]
    shell:
        """
        kaiju -v -t {input.kaijudb}/nodes.dmp -f {input.kaijudb}/kaiju_db.fmi \
            -z {threads} \
            -i {input.r1} \
            -j {input.r2} \
            -o {output.fout}
        """
