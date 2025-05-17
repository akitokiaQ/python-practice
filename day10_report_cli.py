from pathlib import Path
import random, datetime, os, argparse, logging, sys

# ---------- 0. ロガー設定 ----------
LOG_FILE = "app.log"
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

console_h = logging.StreamHandler()
console_h.setFormatter(formatter)

file_h = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_h.setFormatter(formatter)

logger = logging.getLogger("report_cli")
logger.setLevel(logging.INFO)          # デフォルト
logger.addHandler(console_h)
logger.addHandler(file_h)

# ---------- 1. CLI 解析 ----------
parser = argparse.ArgumentParser(description="Generate daily report file")
parser.add_argument("--date", help="Date in YYYY-MM-DD (default: today)")
parser.add_argument("--id",   type=int, help="4-digit ID (default: random)")
parser.add_argument("--verbose", "-v", action="store_true",
                    help="Show debug logs")
args = parser.parse_args()

if args.verbose:
    logger.setLevel(logging.DEBUG)
    logger.debug("Verbose mode ON")

# ---------- 2. 日付・ID 決定 ----------
try:
    date_obj = (datetime.date.fromisoformat(args.date)
                if args.date else datetime.date.today())
except ValueError as e:
    parser.error("日付は YYYY-MM-DD 形式で指定してください")

today  = date_obj.isoformat()
log_id = args.id if args.id else random.randint(1000, 9999)
logger.debug(f"today={today}, id={log_id}")

# ---------- 3. パス組み立て ----------
log_dir  = Path("logs") / today
os.makedirs(log_dir, exist_ok=True)
log_path = log_dir / f"log_{log_id}.txt"

# ---------- 4. ファイル書き込み ----------
try:
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"date={today}\n")
        f.write(f"id={log_id}\n")
    logger.info(" 日報ファイルを作成 → %s", log_path)
except OSError as e:
    logger.exception("ファイル書き込みに失敗しました")
    sys.exit(1)