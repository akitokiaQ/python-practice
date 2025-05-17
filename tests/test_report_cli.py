# tests/test_report_cli.py
import subprocess, json, sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "day10_report_cli.py"

def test_cli_generates_file(tmp_path):
    """--id 5555 で実行するとファイルが出来ることを確認"""
    logs_dir = tmp_path / "logs"
    date = "2099-01-01"          # 将来の日付で衝突を避ける
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--date", date, "--id", "5555"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    expected = logs_dir / date / "log_5555.txt"
    assert expected.exists(), f"{expected} が生成されていない"