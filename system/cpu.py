import psutil


def prime_cpu():
    """CPU使用率の差分計測を初期化する。"""
    psutil.cpu_percent(interval=None)
    psutil.cpu_percent(interval=None, percpu=True)


def read_cpu():
    """CPU全体と論理CPUごとの使用率を返す。"""
    return psutil.cpu_percent(interval=None), psutil.cpu_percent(interval=None, percpu=True)
