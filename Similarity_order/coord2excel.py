import os
import pandas as pd
import re
from tqdm import tqdm

folder_path = './input'
output_dir = "excel"
os.makedirs(output_dir, exist_ok=True)

coord_files = [f for f in os.listdir(folder_path) if f.endswith('.coord')]

for filename in tqdm(coord_files, desc="Processing .coord files"):
    excel_filename = os.path.splitext(filename)[0] + '.xlsx'
    excel_path = os.path.join(output_dir, excel_filename)

    # 如果对应的Excel已经存在，则跳过
    if os.path.exists(excel_path):
        print(f"{excel_path}已存在，跳过")
        continue

    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    data = []
    for line in lines[5:]:
        parts = re.split(r'[ \t|]+', line.strip())
        data.append(parts)

    df = pd.DataFrame(data)


    # print(f"\n{filename}")
    # print("各行字段数量统计：")
    # print(pd.Series([len(row) for row in data]).value_counts())
    # print("DataFrame 总列数：", df.shape[1])

    if df.shape[1] >= 11:
        if df.shape[1] == 14:
            df.drop(columns=[13], inplace=True)

        df.drop(columns=[8, 9, 10], inplace=True)
        df[[0, 1]] = df[[0, 1]].apply(pd.to_numeric, errors='coerce')
        df[[2, 3]] = df[[2, 3]].apply(pd.to_numeric, errors='coerce')


        for i in range(len(df)):
            if df.iat[i, 0] > df.iat[i, 1]:
                df.iat[i, 0], df.iat[i, 1] = df.iat[i, 1], df.iat[i, 0]
            if df.iat[i, 2] > df.iat[i, 3]:
                df.iat[i, 2], df.iat[i, 3] = df.iat[i, 3], df.iat[i, 2]


        df = df.sort_values(by=0, ascending=True, kind='mergesort').reset_index(drop=True)

        if df.shape[1] != 10:
            raise ValueError(f"列数不匹配，当前为 {df.shape[1]} 列，不能赋值为10个列名")

        df.columns = ['S1', 'E1', 'S2', 'E2', 'Len1', 'Len2', 'IDY', 'SIM', '1', '2']
        df.to_excel(excel_path, index=False)
        print(f"{excel_path}已经处理完毕，并保存成功！")