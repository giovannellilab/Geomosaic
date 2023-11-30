
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
