from abc import ABC, abstractmethod
import time
from contextlib import contextmanager

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print

from .models import Transaction
from .data_manager import get_transaction_manager


@contextmanager
def task_progress(description: str):
    """An utility function to display a progress spinner"""
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


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class AddTransactionCommand(Command):
    def __init__(self, transaction: Transaction):
        self._manager = get_transaction_manager()
        self.transaction = transaction

    def execute(self):
        if self._manager is not None:
            with task_progress(description="Processing.."):
                row = self.transaction.to_sheet_row()
                self._manager.add_transaction(row)
                print(":heavy_check_mark: Transaction was added successfully")
