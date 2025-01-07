
rule run_argsoap_custom:
    input:
        r1=expand("{wdir}/{sample}/{pre_processing}/R1.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        r2=expand("{wdir}/{sample}/{pre_processing}/R2.fastq.gz", pre_processing=config["MODULES"]["pre_processing"], allow_missing=True),
        argsoap_custom_fasta = expand("{argsoap_custom_fasta}", argsoap_custom_fasta = config["EXT_DB"]["argsoap_custom"]["protein_fasta"]),
        argsoap_custom_mapping = expand("{argsoap_custom_mapping}", argsoap_custom_mapping = config["EXT_DB"]["argsoap_custom"]["mapping_file"]),
    output:
        directory("{wdir}/{sample}/{argsoap_custom_output_folder}")
    params:
        local_sample="{sample}",
        user_params=( lambda x: " ".join(filter(None , yaml.safe_load(open(x, "r"))["argsoap_custom"])) ) (config["USER_PARAMS"]["argsoap_custom"]),
    conda: config["ENVS"]["argsoap_custom"]
    threads: config["threads"]
    shell:
        """
        folder_read_link="{output}/symbolic_link"
        
        mkdir -p $folder_read_link

        link_r1="{params.local_sample}_R1.fastq.gz"
        link_r2="{params.local_sample}_R2.fastq.gz"
        ( cd $folder_read_link && ln -s {input.r1} -T $link_r1 )
        ( cd $folder_read_link && ln -s {input.r2} -T $link_r2 )

        args_oap stage_one -i $folder_read_link -o {output} -f fastq -t {threads} --database {input.argsoap_custom_fasta}
        args_oap stage_two -i {output} -t {threads} --database {input.argsoap_custom_fasta} --structure1 {input.argsoap_custom_mapping}

        ( cd $folder_read_link && unlink $link_r1 )
        ( cd $folder_read_link && unlink $link_r2 )
        ( cd {output} && rmdir symbolic_link )
        """
