import pandas as pd
import glob
import os
from tqdm import tqdm

name_path = './input'
name_files = [f for f in os.listdir(name_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']
for folder_name in tqdm(name_files, desc="处理 Excel 文件"):
   base_dir = './split-1'
   output_dir = "tem-file"
   os.makedirs(output_dir, exist_ok=True)

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