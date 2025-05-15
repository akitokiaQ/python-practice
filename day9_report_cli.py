from pathlib import Path
import random, datetime, os, argparse, sys

# ---------- 1. CLI 解析 ----------
parser = argparse.ArgumentParser(description="Generate daily report file")
parser.add_argument("--date", help="Date in YYYY-MM-DD (default: today)")
parser.add_argument("--id", type=int, help="4-digit ID (default: random)")
args = parser.parse_args()

try:
    if args.date:
        date_obj = datetime.date.fromisoformat(args.date)
    else:
        date_obj = datetime.date.today()
except ValueError:
    parser.error("日付は YYYY-MM-DD 形式で指定してください")

today = date_obj.isoformat()
log_id = args.id if args.id else random.randint(1000, 9999)

# ---------- 2. パス組み立て ----------
log_dir = Path("logs") / today
os.makedirs(log_dir, exist_ok=True)
log_path = log_dir / f"log_{log_id}.txt"

# ---------- 3. ファイル書き込み ----------
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"date={today}\n")
    f.write(f"id={log_id}\n")

print("日報ファイルを作成 →", log_path)