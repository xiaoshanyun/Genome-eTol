import os
import pandas as pd
from tqdm import tqdm
from pathlib import Path

def process_excel_files():
    top_output_dir = "./split"
    os.makedirs(top_output_dir, exist_ok=True)
    excel_path = './excel'

    excel_files = [f for f in os.listdir(excel_path) if f.endswith(('.xlsx', '.xls')) and f != 'score.xlsx' and f!= 'overlap protocal.xlsx']

    if not excel_files:
        print("未找到Excel文件")
        return

    for file in tqdm(excel_files, desc="处理 Excel 文件"):
        try:
            print(f"\n正在处理：{file}")
            file_dir = os.path.join(excel_path, file)
            df = pd.read_excel(file_dir, header=0, dtype=str, keep_default_na=False)
            if df.shape[1] < 10:
                print(f"跳过 {file}：文件列数不足10列")
                continue

            col9 = df.iloc[:, 8]
            df['d9'] = col9
            file_stem = Path(file).stem
            output_dir = os.path.join(top_output_dir, f"split_{file_stem}")
            os.makedirs(output_dir, exist_ok=True)

            grouped = df.groupby('d9')
            # print(f"发现组合数：{len(grouped)}")

            file_counter = 1
            for _, group in grouped:
                group_data = group.drop(columns=['d9'])
                output_file = os.path.join(output_dir, f"{file_counter}.xlsx")

                try:
                    group_data.to_excel(output_file, index=False)
                    # print(f"写入：{output_file}（{len(group_data)} 行）")
                    file_counter += 1
                except Exception as e:
                    print(f"写入失败：{output_file}")
                    print(f"错误信息：{e}\n")

        except Exception as e:
            print(f"处理 {file} 时出错：{e}")

    print("\n所有文件处理完成！")

if __name__ == "__main__":
    process_excel_files()
