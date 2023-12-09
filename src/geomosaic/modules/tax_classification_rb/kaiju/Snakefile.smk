
rule run_kaiju:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
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
        
        for level in phylum class order family genus species; do
            kaiju2table \
            -u \
            -t {input.kaijudb}/nodes.dmp \
            -n {input.kaijudb}/names.dmp \
            -r $level \
            -o {output.folder}/$level.tsv \
            {output.fout} ;
        done
        """
