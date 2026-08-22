import os
import shutil
import glob
import pandas as pd
from tqdm import tqdm
from pathlib import Path


def concat(args, delete_judge):
   name_path = Path(os.path.abspath(args.input))
   OUTPUT_DIR = Path(os.path.abspath(args.output))
   base_dir  = Path(os.path.join(OUTPUT_DIR, "num"))
   output_dir  = Path(os.path.join(OUTPUT_DIR, "Genome-eTol_result"))
   tem_file_path = Path(os.path.join(OUTPUT_DIR, "tem-file"))
   split_2_DIR = Path(os.path.join(OUTPUT_DIR, "split-2"))
   split_1_DIR = Path(os.path.join(OUTPUT_DIR, "split-1"))
   os.makedirs(output_dir, exist_ok=True)
   name_files = [f for f in os.listdir(name_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']
   for folder_name in tqdm(name_files, desc="处理 Excel 文件"):
      combined_name = "split_split_" + folder_name.split(".xlsx", 1)[0] + "_合并结果"

      folder_path = os.path.join(base_dir, combined_name)
      files = glob.glob(folder_path + "/*.xlsx")

      final_df = pd.DataFrame()
      for file in files:
         df = pd.concat(pd.read_excel(file, sheet_name=None), ignore_index=True)
         final_df = pd.concat([final_df, df], ignore_index=True)
      fpath = os.path.join(output_dir, folder_name+"_合并结果.xlsx")
      final_df.to_excel(fpath, index=False)
      print("合并完成！")
   if delete_judge == 'False':
      shutil.rmtree(base_dir)
      shutil.rmtree(tem_file_path)
      shutil.rmtree(split_2_DIR)
      shutil.rmtree(split_1_DIR)


if __name__ == "__main__":
    concat()