import os
import shutil
from Bio import SeqIO
from pathlib import Path
from datetime import datetime


def log(msg: str, LOG_PATH: Path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line)

def process_seq_file(seq_path: Path, AA_DIR: Path):
    """处理一个 .seq.txt 文件,并在 seq/ 下生成对应的 .seq.txt 文件。"""
    # 输出文件名：把文件名中的 "seq" 替换成 "seq"
    out_name = seq_path.name.replace("seq", "fasta")
    out_path = AA_DIR / out_name

    outputs = []  # 每个元素是 (header_with_index, subseq)
    
    with seq_path.open("r", encoding="utf-8") as f:
        for record in SeqIO.parse(f, "fasta"):
            rrdna = record.seq.reverse_complement()
            aa_1 = str('>'+record.id+'-1\n'+record.seq[0:].translate().replace('*', 'B'))
            aa_2 = str('>'+record.id+'-2\n'+record.seq[1:].translate().replace('*', 'B'))
            aa_3 = str('>'+record.id+'-3\n'+record.seq[2:].translate().replace('*', 'B'))
            aa_4 = str('>'+record.id+'-4\n'+rrdna[0:].translate().replace('*', 'B'))
            aa_5 = str('>'+record.id+'-5\n'+rrdna[1:].translate().replace('*', 'B'))
            aa_6 = str('>'+record.id+'-6\n'+rrdna[2:].translate().replace('*', 'B'))
            outputs.append((aa_1,aa_2,aa_3,aa_4,aa_5,aa_6))
            
    if outputs:
        with out_path.open("w", encoding="utf-8") as f_out:
            for i, (aa_1,aa_2,aa_3,aa_4,aa_5,aa_6) in enumerate(outputs):
                f_out.write(aa_1 + "\n")
                f_out.write(aa_2 + "\n")
                f_out.write(aa_3 + "\n")
                f_out.write(aa_4 + "\n")
                f_out.write(aa_5 + "\n")
                f_out.write(aa_6 + "\n")

def main(args, delete_judge):
    SEQ_tem_DIR = Path(os.path.abspath(args.output))
    SEQ_DIR = Path(os.path.join(SEQ_tem_DIR, "seq-bac"))
    output_dir  = Path(os.path.join(SEQ_tem_DIR, "Genome-eTol_result"))
    AA_DIR = Path(os.path.join(output_dir, "aa-bac"))
    LOG_PATH = Path(os.path.join(output_dir, "log/aa_bac_extraction.log"))
    os.makedirs(output_dir, exist_ok=True)
    AA_DIR.mkdir(exist_ok=True)
    log("=== New run started ===", LOG_PATH)
    # 遍历 seq 目录下所有以 .seq.txt 结尾的文件
    for seq_file in sorted(SEQ_DIR.glob("*.seq")):
        log(f"[INFO] Processing seq file: {seq_file.name}", LOG_PATH)
        process_seq_file(seq_file, AA_DIR)
        log(f"[INFO] Saved output file: {seq_file.name} ({len(seq_file.name)} records)", LOG_PATH)
    if delete_judge == 'False':
        shutil.rmtree(SEQ_DIR)

if __name__ == "__main__":
    main()
