from rich.columns import Columns
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.console import Group


def meter(value, width=22):
    """使用率を文字列のバーに変換する。"""
    filled = round(max(0, min(100, value)) * width / 100)
    return f'[green]{"█" * filled}[/green][grey35]{"░" * (width - filled)}[/grey35]'


def dashboard(cpu, cores, memory, swap, down, up, history, processes):
    # CPUコア別の表示
    cpu_table = Table.grid(padding=(0, 1))
    cpu_table.add_column(width=8)
    cpu_table.add_column()
    for index, usage in enumerate(cores):
        cpu_table.add_row(f'C{index} {usage:4.0f}%', meter(usage, 16))
    cpu_panel = Panel(cpu_table, title=f'[green]CPU {cpu:.1f}%[/green]', border_style='green', expand=True)

    # メモリ・ネットワーク表示
    mem_table = Table.grid(padding=(0, 1))
    mem_table.add_column()
    mem_table.add_row(f'RAM  {memory.used / 1024**3:.2f} / {memory.total / 1024**3:.2f} GiB')
    mem_table.add_row(meter(memory.percent))
    mem_table.add_row(f'SWAP {swap.used / 1024**3:.2f} GiB')
    mem_table.add_row(f'NET ↓ {down / 1024:.1f} KiB/s')
    mem_table.add_row(f'NET ↑ {up / 1024:.1f} KiB/s')
    mem_panel = Panel(mem_table, title='[cyan]MEMORY / NETWORK[/cyan]', border_style='cyan', expand=True)

    # CPU使用率の履歴（最新60サンプル）
    blocks = '▁▂▃▄▅▆▇█'
    graph = ''.join(blocks[min(7, int(max(0, min(100, v)) / 100 * 8))] for v in history)
    history_panel = Panel(Text(graph or '測定中...', style='green'), title='CPU HISTORY (last 60s)', border_style='green')

    # CPU使用率が高いプロセス
    proc_table = Table(expand=True, box=None)
    proc_table.add_column('PID', width=8)
    proc_table.add_column('PROCESS')
    proc_table.add_column('CPU %', justify='right')
    for pid, name, usage in processes:
        proc_table.add_row(str(pid), name[:40], f'{usage:.1f}')
    proc_panel = Panel(proc_table, title='TOP PROCESSES', border_style='green')

    return Group(Columns([cpu_panel, mem_panel], equal=True, expand=True), history_panel, proc_panel)
