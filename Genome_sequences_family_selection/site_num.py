import os
import pandas as pd
from tqdm import tqdm
import openpyxl


def process_excel(fpath1,fpath2):
    df1 = pd.read_excel(fpath1, header=0)
    df2 = pd.read_excel(fpath2, header=0)
    first = [(r[0], r[1]) for r in df1.iloc[:,0:2].values if pd.notnull(r[0])]
    second = [(r[0], r[1], r[2], r[3], r[4]) for r in df2.iloc[:,0:5].values if pd.notnull(r[0])]
    num = 0
    i_count = 0
    pro_name = str()
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'S'
    sheet['B1'] = 'E'
    sheet['C1'] = 'pro'
    sheet['D1'] = 'pro_num'
    sheet['E1'] = 'Pro_name'
    for i, (s1,e1) in enumerate(first):
        for j, (s2,e2,euk,pro,id) in enumerate(second):
            if not (i_count == i):
                num = 0
                pro_name = str()
            if (s2<=s1<=e1<=e2):
                num = num + 1
                if num == 1:
                    pro_name = str(euk) + "#" + str(id)
                else:
                    pro_name = str(pro_name) + ";" + str(euk) + "#" + str(id)
            i_count = i
        y = [s1,e1,pro,num,pro_name]
        sheet.append(y)
    return sheet

def main():
    name_path = './input'
    name_files = [f for f in os.listdir(name_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']
    for folder_name in tqdm(name_files, desc="处理 Excel 文件"):
        combined_name = "split_split_" + folder_name.split(".xlsx", 1)[0] + "_合并结果"
        base_dir  = "./split-2"
        out_dir = "./num"
        folder_path = os.path.join(base_dir, combined_name)
        out_path = os.path.join(out_dir, combined_name)
        os.makedirs(out_path, exist_ok=True)
        files = [f for f in os.listdir(folder_path) if f.endswith("_1.xlsx") and not f.startswith("~$")]
        for fname in tqdm(files, leave=False, ncols=100):
            input_dir = os.path.join(folder_path, fname)
            output_dir = os.path.join(out_path, fname)
            fpath1 = input_dir.split("_1.xlsx", 1)[0] + "_2.xlsx"
            fpath2 = input_dir.split("_1.xlsx", 1)[0] + "_1.xlsx"
            result = output_dir.split("_1.xlsx", 1)[0] + "_num.xlsx"
            if os.path.exists(result):
                # 已存在同名文件则跳过
                print(f"\n跳过 {fname}{result} ，已存在")
                continue
            Result1 = []

            try:
                Result1 = process_excel(fpath1,fpath2)
            except Exception as e:
                print(f"处理失败：{fpath1} -> {e}")
            if Result1:
                value1 = Result1.values
                df1 = pd.DataFrame(value1)
                df1.drop_duplicates(keep='first',inplace=True)
                df1.to_excel(result, index=False, header=False)
                print(f"\n已保存到: {result}\n")
            else:
                print(f"处理失败：{result} -> {e}")

        print("全部完成！")

if __name__ == "__main__":
    main()
