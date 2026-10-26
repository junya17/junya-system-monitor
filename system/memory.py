import re
import subprocess
import psutil


def read_memory():
    """RAMとSwapの統計情報を取得する。"""
    return psutil.virtual_memory(), psutil.swap_memory()


def read_vm_stat():
    """macOSのvm_statを取得。取得失敗時はNoneを返す。"""
    try:
        output = subprocess.run(
            ["/usr/bin/vm_stat"], capture_output=True, text=True,
            timeout=3, check=True
        ).stdout
        match = re.search(r"page size of (\d+) bytes", output)
        page_size = int(match.group(1)) if match else 16384
        counters = {}
        for line in output.splitlines():
            if ":" not in line:
                continue
            key, raw = line.split(":", 1)
            number = re.search(r"(\d+)", raw.replace(".", ""))
            if number:
                counters[key.strip()] = int(number.group(1))
        return {"page_size": page_size, "counters": counters}
    except (OSError, subprocess.SubprocessError, ValueError):
        return None
