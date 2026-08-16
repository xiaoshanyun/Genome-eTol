from pathlib import Path
from datetime import datetime
from Bio import SeqIO

SEQ_DIR = Path("seq-euk")
AA_DIR = Path("aa-euk")
LOG_PATH = Path("aa_euk_extraction.log")  


AA_DIR.mkdir(exist_ok=True)

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line)
    print(msg)

def process_seq_file(seq_path: Path):
    """处理一个 .seq.txt 文件,并在 seq/ 下生成对应的 .seq.txt 文件。"""
    # 输出文件名：把文件名中的 "seq" 替换成 "seq"
    out_name = seq_path.name.replace("seq", "fasta")
    out_path = AA_DIR / out_name

    outputs = []  # 每个元素是 (header_with_index, subseq)
    
    with seq_path.open("r", encoding="utf-8") as f:
        for record in SeqIO.parse(f, "fasta"):
            rrdna = record.seq.reverse_complement()
            aa_1 = str('>'+record.id+'-1\n'+record.seq[0:].translate())
            aa_2 = str('>'+record.id+'-2\n'+record.seq[1:].translate())
            aa_3 = str('>'+record.id+'-3\n'+record.seq[2:].translate())
            aa_4 = str('>'+record.id+'-4\n'+rrdna[0:].translate())
            aa_5 = str('>'+record.id+'-5\n'+rrdna[1:].translate())
            aa_6 = str('>'+record.id+'-6\n'+rrdna[2:].translate())
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


def main():
    log("=== New run started ===")
    # 遍历 seq 目录下所有以 .seq.txt 结尾的文件
    for seq_file in sorted(SEQ_DIR.glob("*.seq")):
        log(f"[INFO] Processing seq file: {seq_file.name}")
        process_seq_file(seq_file)

if __name__ == "__main__":
    main()
