from Bio import SeqIO
import numpy as np
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import os
from tqdm import tqdm

def combine(path):
    x = ""
    i = 1
    j = 1
    combine_list = []
    delete_list = []
    first_list = []
    second_list = []
    sequences = SeqIO.parse(path, "fasta")
    sequence_count = len(list(sequences))
    for record in SeqIO.parse(path,"fasta"):
        if record.id[0:3] == "bac":
            x = record.id
            x_rev = x[::-1]
            start_index = x_rev.find("_")
            before_rev_words = x_rev[start_index+1:].strip()
            before_words = before_rev_words[::-1]
            if i == 1:
                leng = len(record.seq)
            else:
                if before_words == y:
                    if j == 1:
                        if len(first_list) != 0:
                            second_list.append(first_list)
                        first_list = []
                        first_list.append(y_record)
                        j = 2
                    first_list.append(record)
                else:
                    j = 1
            y_record = record
            y = before_words
        if i == sequence_count:
            second_list.append(first_list)
        i += 1
    for m in second_list:
        for n in range(len(m)):
            forward_euk = m[n]
            for_id = forward_euk.id
            for_seq = forward_euk.seq
            for o in range(n + 1, len(m)):
                behind_euk = m[o]
                beh_seq = behind_euk.seq
                beh_id = behind_euk.id
                judge_num = 1
                score_x = 1
                score_y = -1
                dupli = 0
                for p in range(leng):
                    if for_seq[p] !="-" and beh_seq[p] !="-" and for_seq[p] != beh_seq[p]:
                        judge_num = 0
                        break
                    else:
                        if for_seq[p] =="-" and beh_seq[p] != "-":
                            score_x = -1
                            dupli = 1
                        if for_seq[p] !="-" and beh_seq[p] == "-":
                            score_y = 1
                            dupli = 1
                score = score_x + score_y
                if judge_num == 1:
                    if score == 0:
                        if dupli == 1:
                            combine_id = for_id + " " + beh_id
                            combine_list.append(combine_id)
                    if score < 0:
                        delete_list.append(for_id)
                    if score > 0:
                        delete_list.append(beh_id)
    return combine_list, delete_list

def main():
    comb_dir = "./combine"
    delete_dir = "./delete"
    input_dir = "./input-py"
    os.makedirs(comb_dir, exist_ok=True)
    os.makedirs(delete_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".fasta") and not f.startswith("~$")]
    
    for fname in tqdm(files, leave=False, ncols=100):
        fpath = os.path.join(input_dir, fname)
        comb, delete= combine(fpath)
        file_name, end_name = os.path.splitext(fname)
        combine_list_path = os.path.join(comb_dir, "combine_"+file_name+".fasta.txt")
        delete_list_path = os.path.join(delete_dir, "delete_"+file_name+".fasta.txt")
        if len(comb) > 0:
            with open(combine_list_path, "w", encoding="utf-8") as f:
                for item in comb:
                    f.write(item+'\n')
        if len(delete) > 0:
            with open(delete_list_path, "w", encoding="utf-8") as f:
                for item in delete:
                    f.write(item+'\n')

if __name__ == "__main__":
    main()