import psutil


def read_network(previous, elapsed):
    """累積バイト数の差分から1秒あたりの通信速度を計算する。"""
    current = psutil.net_io_counters()
    down = max(0, current.bytes_recv - previous.bytes_recv) / max(elapsed, 0.001)
    up = max(0, current.bytes_sent - previous.bytes_sent) / max(elapsed, 0.001)
    return current, down, up
