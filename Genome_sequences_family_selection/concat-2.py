import pandas as pd
import glob
import os
from tqdm import tqdm

name_path = './input'
name_files = [f for f in os.listdir(name_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']
for folder_name in tqdm(name_files, desc="处理 Excel 文件"):
   combined_name = "split_split_" + folder_name.split(".xlsx", 1)[0] + "_合并结果"
   base_dir = './num'
   output_dir = "result"
   os.makedirs(output_dir, exist_ok=True)

   folder_path = os.path.join(base_dir, combined_name)
   files = glob.glob(folder_path + "/*.xlsx")

   final_df = pd.DataFrame()
   for file in files:
      df = pd.concat(pd.read_excel(file, sheet_name=None), ignore_index=True)
      final_df = pd.concat([final_df, df], ignore_index=True)
   fpath = os.path.join(output_dir, folder_name+"_合并结果.xlsx")
   final_df.to_excel(fpath, index=False)
   print("合并完成！")