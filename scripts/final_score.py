import os
import re
import shutil
import pandas as pd
from pathlib import Path


def process_scores(args, delete_judge):
    OUTPUT_DIR = Path(os.path.abspath(args.output))
    output_dir  = Path(os.path.join(OUTPUT_DIR, "Genome-eTol_result"))
    input_dir  = Path(os.path.join(OUTPUT_DIR, "score"))
    base_dir  = Path(os.path.join(OUTPUT_DIR, "split"))
    excel_dir  = Path(os.path.join(OUTPUT_DIR, "excel"))
    output_file  = Path(os.path.join(output_dir, f"final_score.xlsx"))
    os.makedirs(output_dir, exist_ok=True)


    records = []
    
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(('.xlsx', '.xls')):
            continue
        
        filepath = os.path.join(input_dir, filename)
        
        m1 = re.search(r'score_split_(.+?)-', filename)
        part1 = m1.group(1) if m1 else ''
        
        
        m2 = re.search(r'--(.+?)\.delta', filename)
        part2 = m2.group(1) if m2 else ''
        
        
        df = pd.read_excel(filepath, header=0)
        
        
        sum_d = pd.to_numeric(df.iloc[:, 3], errors='coerce').sum()
        sum_e = pd.to_numeric(df.iloc[:, 4], errors='coerce').sum()
        val1 = sum_d
        val2 = sum_e
        
        records.append([part1, part2, val1, val2])
    

    df_out = pd.DataFrame(records, columns=['第一列', '第二列', 'val1', 'val2'])
    
    df_out.to_excel(output_file, index=False)
    print(f'已将结果保存到 {output_file}')
    if delete_judge == 'False':
        shutil.rmtree(input_dir)
        shutil.rmtree(base_dir)
        shutil.rmtree(excel_dir)


if __name__ == '__main__':
    process_scores()
