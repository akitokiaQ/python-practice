from pathlib import Path
import random,datetime,os

today = datetime.date.today().isoformat()
log_dir = Path("logs") / today
os.makedirs(log_dir,exist_ok=True)

log_id = random.randint(1000, 9999)
log_path = log_dir / f"log_{log_id}.txt"

with open(log_path,"w",encoding="utf-8")as f:
    f.write(f"date={today}\n")
    f.write(f"id={log_id}\n")

print("日報ファイルを作成→",log_path)
