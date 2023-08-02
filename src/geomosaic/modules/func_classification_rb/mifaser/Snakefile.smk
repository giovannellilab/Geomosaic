
rule download_gs21all:
    params:
        sequences="https://bitbucket.org/bromberglab/mifaser/raw/bbd1ca1d093d8a26060ee83daf2d7f3f5e88bfd0/mifaser/database/GS-21-all/sequences.fasta"
    output:
        gs21all="{wdir}/gs21all/sequences.fasta"
    run:
        shell("curl {params.sequences} -o {output.gs21all}")

rule create_updated_diamond_db:
    input:
        gs21all=expand("{wdir}/gs21all/sequences.fasta", wdir=config["WDIR"])
    output:
        diamond_db=directory("{wdir}/gs21all/GS-21-all")
    params:
        mifaser_path="$CONDA_PREFIX/lib/python3.10/site-packages/mifaser/database",
        local_diamond="-i $CONDA_PREFIX/bin "
    run:
        shell("mifaser --createdb GS-21-all {input.gs21all}")
        shell("cp -r {params.mifaser_path}/GS-21-all {output.diamond_db}")


rule run_mifaser:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["pre_processing"], allow_missing=True),
        diamond_db=expand("{wdir}/gs21all/GS-21-all", wdir=config["WDIR"])
    output:
        directory("{wdir}/{sample}/mifaser")
    threads: 10
    run:
        shell("mifaser -d GS-21-all -l {input.r1} {input.r2} -t {threads} -o {output}")
