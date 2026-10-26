# JUNYA SYSTEM MONITOR v0.5

macOS向けリアルタイム監視。CPUコア、履歴、RAM/Swap、ネットワーク、プロセスCPU/RSS/スレッド数、vm_statの圧縮ページとページアウト速度を表示。

## 更新

既存プロジェクトの `monitor.py`, `system/`, `ui/` をバックアップしてから、このZIPの中身をコピーしてください。`requirements.txt` は `psutil` と `rich`。

```bash
cd ~/junya-system-monitor
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m compileall -q monitor.py system ui
python monitor.py
```

## 注意

- `COMP` は `vm_stat` の `Pages occupied by compressor` × ページサイズから算出した圧縮データの物理占有量の概算です。
- `PAGEOUT` は累積ページアウト数の5秒間差分。macOSの公式メモリプレッシャー指標そのものではありません。
- プロセスの `RSS MiB` は常駐メモリで、プロセス間の共有分を含むことがあります。
- CPU%は複数コアを使用するプロセスでは100%を超えることがあります。
- `vm_stat` の項目が利用できない場合は表示を省略します。
- 小さいターミナルでは表示が切れる場合があります。幅100文字以上、高さ40行以上推奨。
