# Day7: ファイル I/O スモールテスト
"""
with open("scores.txt", "w", encoding="utf-8") as f:
#    f.write("国語,72\n数学,85\n英語,91\n")

# with open("scores.txt", "r", encoding="utf-8") as f:
    data = f.read()

# print("ファイル内容:\n", data)
"""

# 既存のスモールテストここまで
# =========================================

# 1. ファイル -> 辞書に読み込む関数
def read_scores(filepath):
    scores = {}
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            subj, pt = line.strip().split(",")
            scores[subj] = int(pt)
    return scores

# 2. 合計・平均を計算
def calc_total_avg(scores):
    total = sum(scores.values())
    avg   = total / len(scores) if scores else 0
    return total, avg

# 3. レポート出力関数
def write_report(scores, outfile):
    total, avg = calc_total_avg(scores)
    with open(outfile, "w", encoding="utf-8") as f:
        for s, p in scores.items():
            f.write(f"{s}: {p} 点\n")
        f.write(f"---\n合計 {total} 点 / 平均 {avg:.1f} 点\n")
    print(f"合計{total}点/平均{avg:.1f}点")
    print("レポートを書き出しました →", outfile)

# 4. 動かす部分
if __name__ == "__main__":
    import datetime

    scores = read_scores("scores.txt")
    total, avg = calc_total_avg(scores)             
    print(f"合計 {total} 点 / 平均 {avg:.1f} 点")      

    stamp  = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    outfile = f"report_{stamp}.txt"
    write_report(scores, outfile)