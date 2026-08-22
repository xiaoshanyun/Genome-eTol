import os
import glob
import pandas as pd
from tqdm import tqdm
from pathlib import Path


def concat(args):
   name_path = Path(os.path.abspath(args.input))
   OUTPUT_DIR = Path(os.path.abspath(args.output))
   base_dir  = Path(os.path.join(OUTPUT_DIR, "split-1"))
   output_dir  = Path(os.path.join(OUTPUT_DIR, "tem-file"))
   os.makedirs(output_dir, exist_ok=True)
   name_files = [f for f in os.listdir(name_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']
   for folder_name in tqdm(name_files, desc="处理 Excel 文件"):

      folder_path = os.path.join(base_dir, "split_" + folder_name.split(".xlsx", 1)[0])
      files = glob.glob(folder_path + "/*.xlsx")
      concat_df = pd.DataFrame()
      for file in files:
         df = pd.concat(pd.read_excel(file, sheet_name=None), ignore_index=True)
         concat_df = pd.concat([concat_df, df], ignore_index=True)
      concat_df[['EUK1', 'pro']] = concat_df['EUK'].str.split('@', expand=True)
      final_df = pd.DataFrame()
      final_df['S'] = concat_df['S']
      final_df['E'] = concat_df['E']
      final_df['EUK'] = concat_df['EUK1']
      final_df['pro'] = concat_df['pro']
      final_df['ID'] = concat_df['ID']
      fpath = os.path.join(output_dir, "split_" + folder_name.split(".xlsx", 1)[0]+"_合并结果.xlsx")
      final_df.to_excel(fpath, index=False)
      print("合并完成！")

if __name__ == "__main__":
    concat()
