import re
import os
from pathlib import Path
from datetime import datetime


def log(msg: str, LOG_PATH: Path):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}\n"
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(line)


def find_gene_file_for_n(n: str, gene_txt_files):
    """在 gene 文件夹中寻找名字包含 n 的 txt 文件。"""
    gene_file_cache = {}
    if n in gene_file_cache:
        return gene_file_cache[n]

    matches = [p for p in gene_txt_files if n in p.name]
    if not matches:
        gene_file_cache[n] = None
        return None

    matches.sort()
    gene_file_cache[n] = matches[0]
    return matches[0]


def load_gene_lines(path: Path):
    """读取 gene 文件的所有行，带简单缓存。"""
    gene_content_cache = {}
    if path in gene_content_cache:
        return gene_content_cache[path]
    with path.open("r", encoding="utf-8") as f:
        lines = f.readlines()
    gene_content_cache[path] = lines
    return lines


def extract_header_and_sequence(lines, m: str, a: int, b: int):
    # 1. 找 header 行
    header_idx = None
    for i, line in enumerate(lines):
        if m in line:
            header_idx = i
            break
    if header_idx is None:
        return None, None, "m_not_found"

    header_line = lines[header_idx].rstrip("\n")

    # 2. 处理 header 行，只保留 '>' 和 '.' 中间的内容
    if ">" in header_line:
        start_idx = header_line.find(">")
    else:
        start_idx = 0

    dot_idx = header_line.find(".")
    if dot_idx == -1:
        header_processed = header_line[start_idx:]
    else:
        header_processed = header_line[start_idx:dot_idx]

    # 3. 从下一行开始构造序列（直到下一个 header 或文件结束）
    seq_lines = []
    for line in lines[header_idx + 1:]:
        if line.startswith(">"):
            break
        seq_lines.append(line.strip())  # 回车不算字符，这里去掉换行

    full_seq = "".join(seq_lines)
    if not full_seq:
        return header_processed, "", "empty_seq"

    # 4. 按 a,b 提取子序列（1-based）
    max_pos = max(a, b)
    min_pos = min(a, b)

    if max_pos > len(full_seq):
        # 长度不够
        return None, None, "seq_too_short"

    sub = full_seq[min_pos - 1:max_pos]  # 1-based -> 0-based

    if a > b:
        sub = sub[::-1]  # 逆序

    return header_processed, sub, "ok"

def n_name(f):
	F = str(f)
	rf = F[::-1]
	start_str = "atled."
	end_str = rf.find("--")
	start_index = rf.index(start_str) + len(start_str)
	# 提取出目标文本
	target = rf[start_index:end_str].strip()
	return str(target[::-1])

def process_coord_file(coord_path: Path, SEQ_DIR: Path, gene_txt_files: list, LOG_PATH: Path):
    """处理一个 .coord.txt 文件，并在 seq/ 下生成对应的 .seq.txt 文件。"""
    # 输出文件名：把文件名中的 "coord" 替换成 "seq"
    out_name = coord_path.name.replace("coord", "seq")
    out_path = SEQ_DIR / out_name

    outputs = []  # 每个元素是 (header_with_index, subseq)

    # 在一个 coord 文件内部统计 header 出现次数
    header_counter = {}  # key: base_header_processed, value: count

    with coord_path.open("r", encoding="utf-8") as f:
        n = n_name(f)
    with coord_path.open("r", encoding="utf-8") as f:
        for line in f:
            raw_line = line.rstrip("\n")
            x = raw_line.strip()
            s = x[::-1]

            n_ab_idx = raw_line.find("|")
            if n_ab_idx == -1:
                continue
            x_ab = raw_line[n_ab_idx+1:]
            # 先取出行首的两个数字 a, b
            m_ab = re.match(r"\s*(\d+)\s+(\d+)", x_ab)
            if not m_ab:
                continue

            a = int(m_ab.group(1))
            b = int(m_ab.group(2))
            
            rowline1_idx = s.find(".")
            if rowline1_idx == -1:
                continue
            rowline2_idx = s.find(".", rowline1_idx + 1)
            if rowline2_idx == -1:
                continue
            x_str = s[rowline1_idx + 1:rowline2_idx-1].strip()

            # 提取 m： ':' 后面到 '.' 前面（不含 '.'）
            m_str = x_str[::-1]
            if not m_str:
                continue

            # 找 gene 文件
            gene_file = find_gene_file_for_n(n, gene_txt_files)
            if gene_file is None:
                # gene 文件都找不到就直接跳过（也可以在这里 log，如果你需要）
                continue

            gene_lines = load_gene_lines(gene_file)
            base_header, subseq, status = extract_header_and_sequence(
                gene_lines, m_str, a, b
            )

            if status == "m_not_found":
                # 没找到对应 m 的 header 行：终端 + log
                log(f"[WARN] m '{m_str}' not found in gene file '{gene_file.name}' ", LOG_PATH)
                log(f"for coord file '{coord_path.name}', a={a}, b={b}, n='{n}'", LOG_PATH)
                continue
            elif status != "ok":
                # 其它情况（empty_seq / seq_too_short），这里选择静默跳过
                continue

            if base_header is None or subseq is None or subseq == "":
                continue

            # 对相同 base_header 加上 _序号
            count = header_counter.get(base_header, 0) + 1
            header_counter[base_header] = count
            header_with_index = f"{base_header}_{count}"

            outputs.append((header_with_index, subseq))

    # 写结果到 seq 文件
    if outputs:
        with out_path.open("w", encoding="utf-8") as f_out:
            for i, (hdr, seq) in enumerate(outputs):
                f_out.write(hdr + "\n")
                f_out.write(seq + "\n")
                if i != len(outputs) - 1:
                    f_out.write("\n")
        # 记录保存了什么文件
        log(f"[INFO] Saved output file: {out_path} ({len(outputs)} records)", LOG_PATH)


def main(args):
    SEQ_TEMP_DIR = Path(os.path.abspath(args.output))
    SEQ_DIR = Path(os.path.join(SEQ_TEMP_DIR, "seq-euk"))
    
    COORD_DIR = Path(os.path.abspath(args.coord))
    GENOME_DIR = Path(os.path.abspath(args.genome))
    output_dir  = Path(os.path.join(SEQ_TEMP_DIR, "Genome-eTol_result"))
    LOG_DIR = Path(os.path.join(output_dir, "log"))
    LOG_PATH = Path(os.path.join(LOG_DIR, "seq_euk_extraction.log"))

    gene_txt_files = list(GENOME_DIR.glob("*.fna"))
    os.makedirs(output_dir, exist_ok=True)
    SEQ_DIR.mkdir(exist_ok=True)
    LOG_DIR.mkdir(exist_ok=True)

    log("=== New run started ===", LOG_PATH)
    # 遍历 coord 目录下所有以 .coord.txt 结尾的文件
    for coord_file in sorted(COORD_DIR.glob("*.coord")):
        log(f"[INFO] Processing coord file: {coord_file.name}", LOG_PATH)
        process_coord_file(coord_file, SEQ_DIR, gene_txt_files, LOG_PATH)


if __name__ == "__main__":
    main()
