import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def check_overlap(intervals):
    """简易重叠检测：只要任意两区间相交即返回 True"""
    for i, (s1,e1) in enumerate(intervals):
        for j, (s2,e2) in enumerate(intervals[i+1:], start=i+1):
            if ((e1 >= s2 and e2 >= s1) or (e2 >= s1 and e1 >= s2)):
                return 1
    return 0

def process_excel(path):
    data = []
    df2 = pd.DataFrame(data)
    df = pd.read_excel(path, header=0)
    df2['S'] = df['S']
    df2['E'] = df['E']
    df2.sort_values(by='E', ascending=True)
    df2.sort_values(by='S', ascending=True)
    df3 = df2.sort_values(by='S', ascending=True)
    site = [(r[0], r[1]) for r in df3.iloc[:,0:2].values if pd.notnull(r[0])]
    has_ov = check_overlap(site)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet['A1'] = 'S'
    sheet['B1'] = 'E'
    if has_ov != 0:
        site_y = []
        i = 0
        i_num = len(site) - 1 
        #print(i_num)
        k = []
        while i <= i_num:
            site_z = []
            site_y = site[i]
            s1 = site_y[0]
            e1 = site_y[1]
            site_z.append(s1)
            site_z.append(e1)
            result = []
            k = []
            if i < i_num:
                for j, (s2,e2) in enumerate(site[i+1:], start=i+1):
                    if e1 >= s2:
                        site_z.append(s2)
                        site_z.append(e2)
                        e1 = max(e1,e2)
                        if j == i_num:
                            i = j + 1
                            k = list(set(site_z))
                            k = sorted(k)
                            for m in range(len(k) - 1):
                                result = k[m:m+2]
                                if m != len(k) - 1:
                                    s1 = result[0]
                                    e1 = result[1]
                                    if e1 - s1 > 2:
                                        if e1 % 3 == 0:
                                            e1 = e1 -1
                                        if (s1 + 1) % 3 == 0:
                                            s1 = s1 + 1
                                        result = [s1,e1]
                                    else:
                                        result = []
                                sheet.append(result)
                            break
                    else:
                        if j <= i_num:
                            k = list(set(site_z))
                            k = sorted(k)
                            for m in range(len(k) - 1):
                                result = k[m:m+2]
                                if j - i != 1:
                                    if m != len(k) - 1:
                                        s1 = result[0]
                                        e1 = result[1]
                                        if e1 - s1 > 2:
                                            if e1 % 3 == 0:
                                                e1 = e1 -1
                                            if (s1 + 1) % 3 == 0:
                                                s1 = s1 + 1
                                            result = [s1,e1]
                                        else:
                                            result = []
                                sheet.append(result)
                            i = j
                        break
            else:
                sheet.append(site_z)
                i = i + 1
            site_z = []
        values = sheet.values
        df5 = pd.DataFrame(values)
        return df5
    else:
        for i,(s,e) in enumerate(site):
            sheet.append([s,e])
        values = sheet.values
        df5 = pd.DataFrame(values)
        return df5

def main():
    name_path = './input'
    name_files = [f for f in os.listdir(name_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']
    for folder_name in tqdm(name_files, desc="处理 Excel 文件"):
        combined_name = "split_split_" + folder_name.split(".xlsx", 1)[0] + "_合并结果"
        print(combined_name)
        base_dir  = "./split-2"
        folder_path = os.path.join(base_dir, combined_name)
        print(folder_path)
        files = [f for f in os.listdir(folder_path) if f.endswith("_1.xlsx") and not f.startswith("~$")]

        for fname in tqdm(files, leave=False, ncols=100):
            fpath = os.path.join(folder_path, fname)
            first_path = os.path.join(folder_path, fname)
            result = first_path.split("_1.xlsx", 1)[0] + "_2.xlsx"
            try:
                v1 = process_excel(fpath)
                v1.drop_duplicates(keep='first',inplace=True)
                v1.dropna(axis=0,how="all",inplace=True)
                #print(v1)
                v1.to_excel(result, index=False, header=False)
                print(f"\n已保存到: {result}\n")
            except Exception as e:
                print(f"处理失败：{fpath} -> {e}")
        print("全部完成！")

if __name__ == "__main__":
    main()
