import pandas as pd
import os
from Bio import SeqIO
import numpy as np
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm

def combine(fasta,txt):
    seq_list = pd.DataFrame()
    seq_list['name'] = ""
    seq_list['seq'] = ""
    last_record = list()
    for record in SeqIO.parse(fasta,"fasta"):
        x = record.id
        basic_seq = str(record.seq)
        leng = len(basic_seq)
        list_add = pd.DataFrame({"name": [x],"seq": [basic_seq]})
        seq_list = pd.concat([seq_list, list_add]).reset_index(drop=True)
    all_id = seq_list.iloc[:, [0]]
    df = pd.read_csv(txt, delimiter=' ', header=None)
    df_delete_1 = df.iloc[:, [0]]
    df_delete_1.columns = ['name']
    df_delete_1.columns = ['name']
    df_delete_2 = df.iloc[:, [1]]
    df_delete_2.columns = ['name']
    df_delete = pd.merge(df_delete_1,df_delete_2,how = "outer").drop_duplicates()
    df_delete = df_delete.reset_index(drop=True)
    df_keep = pd.concat([all_id, df_delete, df_delete]).drop_duplicates(subset=['name'], keep=False)
    df_keep = df_keep.reset_index(drop=True)
    df_singal = pd.merge(seq_list,df_keep,on="name").drop_duplicates()
    df_singal = df_singal.reset_index(drop=True)
    for t in range(len(df_singal)):
        singal_name = df_singal.iloc[t,0]
        singal_seq = df_singal.iloc[t,1]
        singal_record = SeqRecord(Seq(singal_seq),id=singal_name,description='')
        last_record.append(singal_record)
    x = df[0]
    y = df[1]
    df_list = pd.DataFrame()
    df_list['name'] = ""
    df_list['x_fullname'] = ""
    df_list['y_fullname'] = ""
    df_length = len(df)
    df_last = pd.DataFrame()
    df_last['name'] = ""
    df_last['fullname'] = ""
    for i in range(df_length):
        x_words = x[i]
        x_rev = x_words[::-1]
        start_index = x_rev.find("_")
        before_rev_words = x_rev[start_index+1:].strip()
        before_words = before_rev_words[::-1]
        df_list.loc[i, 'name'] = before_words
        df_list.loc[i, 'x_fullname'] = x_words
    for j in range(df_length):
        y_words = y[j]
        df_list.loc[j, 'y_fullname'] = y_words
    grouped = df_list.groupby('name')
    for name, group in grouped:
        id_add_list = list()
        while len(group)>0:
            group = group.reset_index(drop=True)
            id_1_list = list()
            id_1_list.append(np.str_(group.iloc[0,1]))
            id_1_list.append(np.str_(group.iloc[0,2]))
            count = 1
            df_txt = pd.DataFrame()
            df_txt['name'] = ""
            while count == 1:
                count = 0
                group_len = len(group)
                k_list = list()
                for k in range(1,group_len):
                    id_2_list = list()
                    id_2_list.append(np.str_(group.iloc[k,1]))
                    id_2_list.append(np.str_(group.iloc[k,2]))
                    id_add_list = np.concatenate((id_1_list, id_2_list))
                    id_remove_dupli = list(set(id_add_list))
                    if len(id_remove_dupli) - len(id_1_list) < 2:
                        id_1_list = id_remove_dupli
                        k_list.append(k)
                        group = group.reset_index(drop=True)
                        count = 1
                for k in k_list:
                    group = group.drop(k)
            if count == 0:
                for q in range(len(id_1_list)):
                    df_txt.loc[q, 'name'] = id_1_list[q]
            df_combine = pd.merge(seq_list,df_txt,on = "name")
            df_combine['for_name'] = ""
            df_combine['id'] = ""
            basic_name = df_combine.iloc[0,0]
            basic_seq = df_combine.iloc[0,1]
            for r in range(1,len(df_combine)):
                add_seq = df_combine.iloc[r,1]
                name = df_combine.iloc[r,0]
                name_rev = name[::-1]
                start_index = name_rev.find("_")
                id_rev_words = name_rev[:start_index].strip()
                id_words = id_rev_words[::-1]
                basic_name = basic_name + "+" + id_words
                z_seq = ""
                for s in range(leng):
                    if add_seq[s] =="-" and basic_seq[s] == "-":
                        z_seq = z_seq + "-"
                    if add_seq[s] =="-" and basic_seq[s] != "-":
                        z_seq = z_seq + basic_seq[s]
                    if add_seq[s] !="-" and basic_seq[s] == "-":
                        z_seq = z_seq + add_seq[s]
                    if add_seq[s] !="-" and basic_seq[s] != "-":
                        z_seq = z_seq + add_seq[s]
                basic_seq = z_seq
            basic_record = SeqRecord(Seq(basic_seq),id=basic_name,description='')
            last_record.append(basic_record)
            group = group.drop(0)
            group = group.reset_index(drop=True)
    return last_record


def main():
    input_dir = "./input-py"
    combine_dir = "./combine"
    result_dir = "./combined"
    os.makedirs(result_dir, exist_ok=True)
    files = [f for f in os.listdir(input_dir) if f.endswith(".fasta") and not f.startswith("~$")]
    for fname in tqdm(files, leave=False, ncols=100):
        fpath = os.path.join(input_dir, fname)
        txtpath = os.path.join(combine_dir, "combine_"+fname+".txt")
        result_path = os.path.join(result_dir, fname)
        result= combine(fpath,txtpath)
        SeqIO.write(result, result_path, "fasta")

if __name__ == "__main__":
    main()