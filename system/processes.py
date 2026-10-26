import psutil


def read_processes(limit=12):
    """CPU上位のプロセス。CPU%はプロセス単位で100%を超える場合がある。"""
    result = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'num_threads']):
        try:
            info = proc.info
            rss = info['memory_info'].rss if info['memory_info'] else 0
            result.append((info['pid'], info['name'] or '?',
                           info['cpu_percent'] or 0.0, rss,
                           info['num_threads'] or 0))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return sorted(result, key=lambda row: row[2], reverse=True)[:limit]
