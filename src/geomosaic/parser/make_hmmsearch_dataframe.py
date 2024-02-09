
from geomosaic._utils import GEOMOSAIC_PROCESS
from Bio import SearchIO
import pandas as pd
from tqdm import tqdm


def make_hmmsearch_dataframe(list_hmmsearch_outputs):
    l = []
    print(f"{GEOMOSAIC_PROCESS}: Processing all the output results from hmmsearch...")
    for pathfilename in tqdm(list_hmmsearch_outputs):
        with open (pathfilename,"r") as handle: 
            for record in SearchIO.parse(handle, 'hmmer3-text'):
                l += parse_hmmsearch_output(record)
    
    df = pd.DataFrame(l, columns=["HMM_model", "orf_id", "HMM_length", "hmm_start", "hmm_end", 
                              "identical_match", "conserved_match", "perc_identical", "perc_conserved",
                              "bitscore", "indipendent_evalue", "conditional_evalue", "gaps", "sequence_match" ])

    df.sort_values(by="perc_identical", ascending=False, inplace=True)
    return df


def parse_hmmsearch_output(record):
    rows = []
    
    for i in record.hsps:
        model_id = i.query_id
        orf_id = i.hit_id
        model_len = record.seq_len
        model_start = i.query_range[0]
        model_end = i.query_range[1]
        sequence_match = i.aln_annotation["similarity"]
        identical_match = sum([1 if c not in ("+", " ") else 0 for c in sequence_match])
        conserved_match = sum([1 if c != " " else 0 for c in sequence_match])
        gaps = sum([1 for c in str(i.hit.seq) if c == "-"])
        perc_identical = (identical_match/model_len)*100
        perc_conserved = (conserved_match/model_len)*100
        bitscore = i.bitscore
        indipendent_evalue = i.evalue
        conditional_evalue = i.evalue_cond
        
        match_res = [model_id, orf_id, model_len, model_start, model_end, 
                     identical_match, conserved_match, perc_identical, perc_conserved, 
                     bitscore, indipendent_evalue, conditional_evalue, gaps, sequence_match ]
        
        rows.append(match_res)
    
    return rows
