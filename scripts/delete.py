import os
import shutil
from tqdm import tqdm
from Bio import SeqIO
from pathlib import Path


def remove(fasta,txt):
    remove_list = []
    with open(txt, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i in lines:
            remove_list.append(i.strip("\n"))
    last_record = list()
    for record in SeqIO.parse(fasta,"fasta"):
        if record.id not in remove_list:
            last_record.append(record)
    return last_record


def main(args):
    input_dir1 = Path(os.path.abspath(args.input1))
    input_dir2 = Path(os.path.abspath(args.input2))
    OUTPUT_DIR = Path(os.path.abspath(args.output))
    delete_dir  = Path(os.path.join(input_dir2, "delete"))
    result_dir  = Path(os.path.join(OUTPUT_DIR, "deleted"))
    os.makedirs(result_dir, exist_ok=True)
    input_files = [f for f in os.listdir(input_dir1) if f.endswith(".fasta") and not f.startswith("~$")]
    delete_files = [f for f in os.listdir(delete_dir) if f.endswith(".fasta") and not f.startswith("~$")]
    for fname in tqdm(input_files, leave=False, ncols=100):
        if fname not in delete_files:
            fpath = os.path.join(input_dir1, fname)
            shutil.copy(fpath, result_dir)
        else:
            fpath = os.path.join(input_dir1, fname)
            txtpath = os.path.join(delete_dir, fname)
            result_path = os.path.join(result_dir, fname)
            result= remove(fpath,txtpath)
            SeqIO.write(result, result_path, "fasta")

if __name__ == "__main__":
    main()