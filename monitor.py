import time
from collections import deque
import psutil
from rich.live import Live
from system.cpu import prime_cpu, read_cpu
from system.memory import read_memory, read_vm_stat
from system.network import read_network
from system.processes import read_processes
from ui.dashboard import dashboard


def main():
    # CPUとネットワークの差分計測を初期化
    prime_cpu()
    previous_net = psutil.net_io_counters()
    previous_time = time.monotonic()
    history = deque(maxlen=60)

    # vm_statは比較的重い外部コマンドなので5秒ごとに更新
    vm_data = None
    previous_pageouts = None
    previous_vm_time = None
    pageouts_per_sec = None
    next_vm_read = 0

    with Live(screen=True, refresh_per_second=4) as live:
        while True:
            time.sleep(1)
            now = time.monotonic()
            cpu, cores = read_cpu()
            memory, swap = read_memory()
            previous_net, down, up = read_network(previous_net, now - previous_time)
            previous_time = now
            history.append(cpu)

            if now >= next_vm_read:
                new_vm = read_vm_stat()
                if new_vm is not None:
                    pageouts = new_vm['counters'].get('Pageouts')
                    if (pageouts is not None and previous_pageouts is not None
                            and previous_vm_time is not None):
                        elapsed = max(now - previous_vm_time, 0.001)
                        pageouts_per_sec = max(0, pageouts - previous_pageouts) / elapsed
                    previous_pageouts = pageouts
                    previous_vm_time = now
                    vm_data = new_vm
                next_vm_read = now + 5

            processes = read_processes()
            live.update(dashboard(cpu, cores, memory, swap, down, up,
                                  history, processes, vm_data, pageouts_per_sec))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Monitor stopped.')
