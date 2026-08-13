import os
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

def compute_adjusted_scores_sweepline(df):
    df[['S1','E1','Len','IDY','SIM']] = df[['S1','E1','Len','IDY','SIM']].apply(pd.to_numeric, errors='coerce')
    intervals = list(df[['S1','E1','SIM','IDY']].itertuples(index=False, name=None))

    events = []
    event = []

    for i, (s, e, sim, idy) in enumerate(intervals):
        events.append((s, +1, i, sim, idy))
        events.append((e, -1, i, sim, idy))
        event.append((s, e, sim, idy))
    events.sort()
    event.sort()
        
    active = set()
    ac = set ()
    prev_pos = None
    overlap_score_sim = 0
    overlap_score_idy = 0
    unoverlap = defaultdict(float)

    for pos, delta, idx, sim, idy in events:
        if prev_pos is not None and pos > prev_pos and active:
            seg_len = pos - prev_pos
            #s=[]
            if len(active) >= 1:
                #for i, (s, e, sim, idy) in ac:
                    # h=len(ac)
                    #length = max(s,e)-min(s,e)
                    #idy = df.iloc[i]['IDY']
                    #overlap_score_sim += 1/h * length * sim
                    #overlap_score_idy += 1/h * length * idy
            #return overlap_score_sim, overlap_score_idy
                sims = [intervals[i][2] for i in active]
                idys = [intervals[i][3] for i in active]
                weight_sim = sum(sims)
                weight_idy = sum(idys)
                s=0.5*len(events)
            #m = [max(i) for i in active]
                overlap_score_sim += 1/s*weight_sim * seg_len
                overlap_score_idy += 1/s*weight_idy * seg_len
            else:
                only = next(iter(active))
                unoverlap[only] += seg_len
        if delta > 0:
            active.add(idx)
        else:
            active.remove(idx)
        prev_pos = pos

    val1 = val2 = 0
    for i, (_s, _e, sim, idy) in enumerate(intervals):
        length = unoverlap[i]
        idy = df.iloc[i]['IDY']
        val1 += 1 * length * idy
        val2 += 1 * length * sim

    val1 += overlap_score_idy
    val2 += overlap_score_sim
    return val1, val2

def check_overlap(intervals):
    """简易重叠检测：只要任意两区间相交即返回 True"""
    pair = []
    for i, (s1, e1) in enumerate(intervals):
        for j, (s2, e2) in enumerate(intervals[i+1:], start=i+1):
            if not (e1 <= s2 or e2 <= s1):
                return True
    return False

def process_excel(path):
    df = pd.read_excel(path, header=0)
    first = [(r[0], r[1]) for r in df.iloc[:,0:2].values if pd.notnull(r[0])]
    has_ov = check_overlap(first)

    col9  = str(df.iloc[0,8]) if df.shape[1] > 8 else ""
    col10 = str(df.iloc[0,9]) if df.shape[1] > 9 else ""

    if has_ov:
        df = df.rename(columns={
            df.columns[0]:'S1', df.columns[1]:'E1',
            df.columns[4]:'Len', df.columns[6]:'IDY', df.columns[7]:'SIM'
        })
        val1, val2 = compute_adjusted_scores_sweepline(df)
        pairs = []
        for i,(s1,e1) in enumerate(first):
            for j,(s2,e2) in enumerate(first[i+1:], start=i+1):
                if not (e1<=s2 or e2<=s1):
                    pairs.append(f"{i+2}-{j+2}")
                    
        overlap_flag = ", ".join(pairs)
    else:
        try:
            val1 = (df.iloc[:,4] * df.iloc[:,6]).sum()
        except:
            val1 = 0
        try:
            val2 = (df.iloc[:,4] * df.iloc[:,7]).sum()
        except:
            val2 = 0
        overlap_flag = "√"

    return [col9, col10, overlap_flag, val1, val2, path]

def main():
    base_dir  = "./split"
    score_dir = "./score"
    os.makedirs(score_dir, exist_ok=True)

    subfolders = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    print(f"共发现 {len(subfolders)} 个文件夹，开始处理...")

    for folder in tqdm(subfolders, desc="处理文件夹", ncols=100):
        out_path = os.path.join(score_dir, f"score_{folder}.xlsx")
        if os.path.exists(out_path):
            # 已存在同名文件则跳过
            print(f"\n跳过 {folder}（{out_path} ，已存在")
            continue

        folder_path = os.path.join(base_dir, folder)
        files = [f for f in os.listdir(folder_path) if f.endswith(".xlsx") and not f.startswith("~$")]

        results = []
        for fname in tqdm(files, leave=False, ncols=100):
            fpath = os.path.join(folder_path, fname)
            try:
                results.append(process_excel(fpath))
            except Exception as e:
                print(f"处理失败：{fpath} -> {e}")

        if results:
            df_out = pd.DataFrame(results,
                columns=["Col9","Col10","Overlap","Val1","Val2","FilePath"])
            df_out.to_excel(out_path, index=False)
            print(f"\n已保存到: {out_path}\n")

    print("全部完成！")

if __name__ == "__main__":
    main()
