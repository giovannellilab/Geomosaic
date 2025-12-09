
rule run_kaiju:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        kaijudb=expand("{kaiju_extdb_folder}", kaiju_extdb_folder=config["EXT_DB"]["kaiju"])
    output:
        folder=directory("{wdir}/{sample}/kaiju"),
        fout="{wdir}/{sample}/kaiju/kaiju.out"
    params:
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["kaiju"])) ) (config["USER_PARAMS"]["kaiju"])
    threads: config["threads"]
    conda: config["ENVS"]["kaiju"]
    shell:
        """
        kaiju -v -t {input.kaijudb}/nodes.dmp -f {input.kaijudb}/kaiju_db.fmi \
            -z {threads} \
            -i {input.r1} \
            -j {input.r2} \
            -o {output.fout}
        
        kaiju2table \
        -u \
        -t {input.kaijudb}/nodes.dmp \
        -n {input.kaijudb}/names.dmp \
        -r phylum \
        -l superkingdom,phylum \
        -o {output.folder}/phylum.tsv \
        {output.fout} ;

        kaiju2table \
        -u \
        -t {input.kaijudb}/nodes.dmp \
        -n {input.kaijudb}/names.dmp \
        -r class \
        -l superkingdom,phylum,class \
        -o {output.folder}/class.tsv \
        {output.fout} ;

        kaiju2table \
        -u \
        -t {input.kaijudb}/nodes.dmp \
        -n {input.kaijudb}/names.dmp \
        -r order \
        -l superkingdom,phylum,class,order \
        -o {output.folder}/order.tsv \
        {output.fout} ;
        
        kaiju2table \
        -u \
        -t {input.kaijudb}/nodes.dmp \
        -n {input.kaijudb}/names.dmp \
        -r family \
        -l superkingdom,phylum,class,order,family \
        -o {output.folder}/family.tsv \
        {output.fout} ;

        kaiju2table \
        -u \
        -t {input.kaijudb}/nodes.dmp \
        -n {input.kaijudb}/names.dmp \
        -r genus \
        -l superkingdom,phylum,class,order,family,genus \
        -o {output.folder}/genus.tsv \
        {output.fout} ;

        kaiju2table \
        -u \
        -t {input.kaijudb}/nodes.dmp \
        -n {input.kaijudb}/names.dmp \
        -r species \
        -l superkingdom,phylum,class,order,family,genus,species \
        -o {output.folder}/species.tsv \
        {output.fout} ;

        """
