from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def meter(value, width=24):
    """使用率を色付きの棒グラフへ変換する。"""
    value = max(0, min(100, value))
    filled = round(value * width / 100)
    return f"[green]{'█' * filled}[/green][grey35]{'░' * (width - filled)}[/grey35]"


def history_graph(history, height=7):
    """各列の高さを使用率に対応させた履歴グラフ。"""
    values = list(history)
    if not values:
        return Text('Collecting samples...', style='dim')
    lines = []
    for row in range(height, 0, -1):
        threshold = (row - 1) * 100 / height
        chars = ''.join('█' if v > threshold else ' ' for v in values)
        lines.append(f'{int(row * 100 / height):3d}│{chars}')
    lines.append('  0└' + '─' * len(values))
    return Text('\n'.join(lines), style='green', no_wrap=True)


def dashboard(cpu, cores, memory, swap, down, up, history, processes,
              vm_data=None, pageouts_per_sec=None):
    # 上段と履歴を固定し、残りの高さをプロセス一覧へ配分
    layout = Layout()
    layout.split_column(
        Layout(name='header', size=3),
        Layout(name='stats', size=13),
        Layout(name='history', size=11),
        Layout(name='processes', ratio=1, minimum_size=10),
    )
    layout['stats'].split_row(
        Layout(name='cpu', ratio=3, minimum_size=35),
        Layout(name='memory', ratio=2, minimum_size=37),
    )
    layout['header'].update(Panel(
        '[bold green]JUNYA SYSTEM MONITOR[/bold green]  [dim]v0.5  •  LIVE  •  Ctrl+C to exit[/dim]',
        border_style='green'))

    cpu_table = Table.grid(padding=(0, 1))
    cpu_table.add_column(width=11)
    cpu_table.add_column()
    for index, usage in enumerate(cores):
        cpu_table.add_row(f'C{index} {usage:5.1f}%', meter(usage))
    layout['cpu'].update(Panel(cpu_table, title=f'[green]CPU {cpu:.1f}%[/green]', border_style='green'))

    mem_table = Table.grid(padding=(0, 1))
    mem_table.add_column()
    mem_table.add_row(f'RAM   {memory.used / 1024**3:.2f} / {memory.total / 1024**3:.2f} GiB')
    mem_table.add_row(meter(memory.percent))
    mem_table.add_row(f'SWAP  {swap.used / 1024**3:.2f} GiB')
    mem_table.add_row(f'DOWN  {down / 1024:.1f} KiB/s')
    mem_table.add_row(f'UP    {up / 1024:.1f} KiB/s')
    if vm_data is not None:
        counters = vm_data['counters']
        compressed = counters.get('Pages occupied by compressor')
        if compressed is not None:
            gib = compressed * vm_data['page_size'] / 1024**3
            mem_table.add_row(f'COMP  {gib:.2f} GiB')
        if pageouts_per_sec is not None:
            mem_table.add_row(f'PAGEOUT {pageouts_per_sec:.1f} pages/s')
    else:
        mem_table.add_row('[dim]vm_stat unavailable[/dim]')
    layout['memory'].update(Panel(mem_table, title='[cyan]MEMORY / NETWORK[/cyan]', border_style='cyan'))

    layout['history'].update(Panel(history_graph(history),
        title='CPU HISTORY · up to 60 samples / ~1s', border_style='green'))

    proc_table = Table(expand=True, box=None, padding=(0, 1))
    proc_table.add_column('PID', width=8)
    proc_table.add_column('PROCESS', overflow='ellipsis')
    proc_table.add_column('CPU %', justify='right', width=9)
    proc_table.add_column('RSS MiB', justify='right', width=10)
    proc_table.add_column('THREADS', justify='right', width=9)
    for pid, name, usage, rss, threads in processes:
        proc_table.add_row(str(pid), name, f'{usage:.1f}', f'{rss / 1024**2:.1f}', str(threads))
    layout['processes'].update(Panel(proc_table, title='TOP PROCESSES', border_style='green'))
    return layout
