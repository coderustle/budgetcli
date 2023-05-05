import time
from contextlib import contextmanager

from rich import box, print
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn


@contextmanager
def task_progress(description: str):
    """A utility function to display a progress spinner"""
    start_time = time.time()
    spinner = SpinnerColumn()
    text = TextColumn("[progress.description]{task.description}")
    try:
        with Progress(spinner, text, transient=True) as progress:
            progress.add_task(description=description, total=None)
            yield
    finally:
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f":sparkles: Completed in {elapsed_time:.2f} seconds")


def get_transaction_table() -> Table:
    """Return table to display the transaction date"""
    table = Table(header_style="blue", box=box.HORIZONTALS)
    table.add_column("Date", no_wrap=True)
    table.add_column("Category", no_wrap=True)
    table.add_column("Description", no_wrap=True)
    table.add_column("Income", no_wrap=True, style="green")
    table.add_column("Outcome", no_wrap=True, style="red")
    return table


def get_category_table() -> Table:
    """Return table to display categories"""
    table = Table(header_style="blue", box=box.HORIZONTALS)
    table.add_column("Category", no_wrap=True)
    return table
