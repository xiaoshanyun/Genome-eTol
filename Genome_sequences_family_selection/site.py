import os
import pandas as pd
from tqdm import tqdm
import numpy as np
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows

def check_overlap1(intervals):
    """简易重叠检测：只要任意两区间相交即返回 True"""
    num = 0
    for i, (s1,e1,idy1,euk1,id1) in enumerate(intervals):
        for j, (s2,e2,idy2,euk2,id2) in enumerate(intervals[i+1:], start=i+1):
            if ((e1 >= s2 and e2 >= s1) or (e2 >= s1 and e1 >= s2)):
                num = num + 1
    return num

def check_overlap2(intervals):
    """简易重叠检测：只要任意两区间相交即返回 True"""
    num = 0
    for i, (s1,e1,euk1,id1) in enumerate(intervals):
        for j, (s2,e2,euk2,id2) in enumerate(intervals[i+1:], start=i+1):
            if ((e1>=s2 and e2>=s1) or (e2>=s1 and e1>=s2)):
                num = num + 1
    return num

def process_excel(path):
    data = []
    df2 = pd.DataFrame(data)
    df = pd.read_excel(path, header=0)
    df2['S'] = df['S']
    df2['E'] = df['E']
    df2['EUK'] = df['EUK']
    df2['ID'] = df['ID']
    df2.sort_values(by='S', ascending=True)
    df3 = df.sort_values(by='S', ascending=True)
    col_num = df.shape[1]
    if col_num > 4:
        first = [(r[0], r[1], r[2], r[3], r[4]) for r in df3.iloc[:,0:5].values if pd.notnull(r[0])]
        has_ov = check_overlap1(first)
        sheet = []
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        if has_ov != 0:
            e = []
            f = []
            x = []
            y = []
            r = []
            m = []
            n = []
            k = []
            w = []
            l = []
            v = []
            sheet['A1'] = 'S'
            sheet['B1'] = 'E'
            sheet['C1'] = 'EUK'
            sheet['D1'] = 'ID'
            s1_1 = e1_1 = s1_2 = e1_2 = s2_1 = e2_1 = s2_2 = e2_2 = 0
            for i,(s1,e1,idy1,euk1,id1) in enumerate(first):
                for j,(s2,e2,idy2,euk2,id2) in enumerate(first[i+1:], start=i+1):
                    f.append(i)
                    f.append(j)
                    if (e1 >= s2 and e2 >= s1) or (e2 >= s1 and e1 >= s2):                    
                        if idy1 >= idy2:
                            if s1 == s2 and e1 == e2:
                                s2 = e2 = 0
                                y = [s1,e1,euk1,id1]
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            elif s2 < s1 <= e1 <= e2 or s2 <= s1 <= e1 < e2:
                                if s1 != s2 and e1 != e2:
                                    s2_1 = s2
                                    e2_1 = s1 - 1
                                    s2_2 = e1 + 1
                                    e2_2 = e2
                                    x = [s2_1,e2_1,euk2,id2]
                                    y = [s2_2,e2_2,euk2,id2]
                                    r = [s1,e1,euk1,id1]
                                    sheet.append(x)
                                    sheet.append(y)
                                    sheet.append(r)
                                    m = i
                                    n = j
                                    e.append(m)
                                    e.append(n)
                                elif e1 == e2:
                                    e2 = s1 - 1
                                    x = [s2,e2,euk2,id2]
                                    y = [s1,e1,euk1,id1]
                                    sheet.append(x)
                                    sheet.append(y)
                                    m = i
                                    n = j
                                    e.append(m)
                                    e.append(n)
                                else:
                                    s2 = e1 + 1
                                    x = [s2,e2,euk2,id2]
                                    y = [s1,e1,euk1,id1]
                                    sheet.append(x)
                                    sheet.append(y)
                                    m = i
                                    n = j
                                    e.append(m)
                                    e.append(n)
                            elif s1 < s2 <= e2 <= e1 or s1 <= s2 <= e2 < e1:
                                s2 = e2 = 0
                                y = [s1,e1,euk1,id1]
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            elif s1 < s2 <= e1 < e2:
                                s2 = e1 + 1
                                x = [s2,e2,euk2,id2]
                                y = [s1,e1,euk1,id1]
                                sheet.append(x)
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            else:
                                e2 = s1 - 1
                                x = [s2,e2,euk2,id2]
                                y = [s1,e1,euk1,id1]
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                        else:
                            if s1 == s2 and e1 == e2:
                                s1 = e1 = 0
                                y = [s2,e2,euk2,id2]
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            elif s1 < s2 <= e2 <= e1 or s1 <= s2 <= e2 < e1:
                                if s1 != s2 and e1 != e2:
                                    s1_1 = s1
                                    e1_1 = s2 - 1
                                    s1_2 = e2 + 1
                                    e1_2 = e1
                                    x = [s1_1,e1_1,euk1,id1]
                                    y = [s1_2,e1_2,euk1,id1]
                                    r = [s2,e2,euk2,id2]
                                    sheet.append(x)
                                    sheet.append(y)
                                    sheet.append(r)
                                    m = i
                                    n = j
                                    e.append(m)
                                    e.append(n)
                                elif s1 == s2:
                                    s1 = e2 + 1
                                    x = [s1,e1,euk1,id1]
                                    y = [s2,e2,euk2,id2]
                                    sheet.append(x)
                                    sheet.append(y)
                                    m = i
                                    n = j
                                    e.append(m)
                                    e.append(n)
                                else:
                                    e1 = s2 - 1
                                    x = [s1,e1,euk1,id1]
                                    y = [s2,e2,euk2,id2]
                                    sheet.append(x)
                                    sheet.append(y)
                                    m = i
                                    n = j
                                    e.append(m)
                                    e.append(n)
                            elif s2 < s1 <= e1 <= e2 or s2 <= s1 <= e1 < e2:
                                s1 = e1 = 0
                                y = [s2,e2,euk2,id2]
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            elif s2 < s1 <= e2 < e1:
                                s1 = e2 + 1
                                x = [s1,e1,euk1,id1]
                                y = [s2,e2,euk2,id2]
                                sheet.append(x)
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            else:
                                e1 = s2 - 1
                                x = [s1,e1,euk1,id1]
                                y = [s2,e2,euk2,id2]
                                sheet.append(x)
                                sheet.append(y)
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                k = list(set(e))
                w = list(set(f))
            l = list(set(w).difference(set(k)))
            for i in l:
                u = first[i]
                v = [u[0],u[1],u[3],u[4]]
                sheet.append(v)
            v = [1,sheet]
        else:
            for row in dataframe_to_rows(df2, index=False, header=True):
                sheet.append(row)
            v = [0,sheet]
    else:
        first = [(r[0], r[1], r[2], r[3]) for r in df2.iloc[:,0:4].values if pd.notnull(r[0])]
        has_ov = check_overlap2(first)
        df = df.rename(columns={
            df.columns[0]:'S', df.columns[1]:'E',
            df.columns[2]:'EUK',df.columns[3]:'ID'
        })
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        if has_ov != 0:
            e = []
            f = []
            x = []
            m = []
            n = []
            j = []
            k = []
            l = []
            v = []
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            sheet['A1'] = 'S'
            sheet['B1'] = 'E'
            sheet['C1'] = 'EUK'
            sheet['D1'] = 'ID'
            for i,(s1,e1,euk1,id1) in enumerate(first):
                for j,(s2,e2,euk2,id2) in enumerate(first[i+1:], start=i+1):
                    f.append(i)
                    f.append(j)
                    row1 = str(euk1) + "_" + str(id1)
                    row2 = str(euk2) + "_" + str(id2)
                    if row1 == row2:
                        if ((e1>=s2 and e2>=s1) or (e2>=s1 and e1>=s2)):
                            arr = [s1, e1, s2, e2]
                            if s1 < s2 <= e1 < e2 or s2 < s1 <= e2 < e1:
                                max2 = np.sort(arr)[-2]
                                max3 = np.sort(arr)[-3]
                                x = [max3,max2,euk1,id1]
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            elif s1 == s2 and e1 != e2:
                                max2 = np.sort(arr)[-2]
                                max3 = s2
                                x = [max3,max2,euk1,id1]
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            elif s1 != s2 and e1 == e2:
                                max2 = e1
                                max3 = np.sort(arr)[-3]
                                x = [max3,max2,euk1,id1]
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            else:
                                max2 = e1
                                max3 = s1
                                x = [max3,max2,euk1,id1]
                                m = i
                                n = j
                                e.append(m)
                                e.append(n)
                            sheet.append(x)
                    j = list(set(e))
                    k = list(set(f))
            l = list(set(k).difference(set(j)))
            for i in l:
                u = first[i]
                sheet.append(u)
            v = [1,sheet]
        else:
            for row in dataframe_to_rows(df2, index=False, header=True):
                sheet.append(row)
            v = [0,sheet]
    return v

def main():
    name_path = './input'
    name_files = [f for f in os.listdir(name_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']
    output_judge = ""
    for folder_name in tqdm(name_files):
        base_dir  = "./split-1"
        folder_path = os.path.join(base_dir, "split_" + folder_name.split(".xlsx", 1)[0])
        files = [f for f in os.listdir(folder_path) if f.endswith("_1.xlsx") and not f.startswith("~$")]
        judge = 0
        if len(files) > 0:
            for fname in tqdm(files, leave=False, ncols=100):
                fpath = os.path.join(folder_path, fname)
                result_path = os.path.join(folder_path, fname)
                result = fpath
                end_result = result_path.split("_1.xlsx", 1)[0] + "_end.xlsx"
                try:
                    p = process_excel(fpath)
                except Exception as e:
                    print(f"处理失败：{fpath} -> {e}")
                if p:
                    v1 = p[1]
                    v0 = p[0]
                    os.remove(fpath)
                    if v0 == 1:
                        values = v1.values
                        df1 = pd.DataFrame(values)
                        df1.drop_duplicates(keep='first',inplace=True)
                        df1.dropna(axis=0,how="all",inplace=True)
                        df1.to_excel(result, index=False, header=False)
                        print(f"\n已保存到: {result}\n")
                        judge = 1
                    else:
                        values = v1.values
                        df1 = pd.DataFrame(values)
                        df1.drop_duplicates(keep='first',inplace=True)
                        df1.dropna(axis=0,how="all",inplace=True)
                        df1.to_excel(end_result, index=False, header=False)
                        print(f"\n已保存到: {end_result}\n")
        if judge == 0:
            output_judge = output_judge + folder_name + ": Y\n"
        else:
            output_judge = output_judge + folder_name + ": N\n"

    print("\nOutput:\n" + output_judge)

if __name__ == "__main__":
    main()
