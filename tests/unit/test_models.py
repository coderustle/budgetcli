from datetime import datetime
from decimal import Decimal

from budgetcli.models import Category, Transaction


def test_transaction_instance():
    """Test that a transaction instance is created"""
    transaction = Transaction(
        datetime.now(),
        "Salary",
        "Salary for January",
        Decimal(0.0),
        Decimal(0.0),
    )
    assert isinstance(transaction, Transaction)


def test_transaction_from_sheet_row():
    """Test that a transaction instance is created from a sheet row"""
    transaction = Transaction.from_sheet_row(
        [
            "01/01/2021",
            "category",
            "Salary for January",
            "0.0",
            "1000.0",
        ]
    )
    assert isinstance(transaction, Transaction)

class TestCategoryModel:

    def test_category_instance(self):
        """Test category instance"""
        category = Category(name="Salary")
        assert isinstance(category, Category)
        assert category.name == "salary"

    def test_category_from_sheet_row(self):
        """Test create categor instance from list of string"""
        row = ["salary"]
        category = Category.from_sheet_row(row)
        assert isinstance(category, Category)

    def test_to_sheet_row(self):
        """Test convert category to sheet row"""
        category = Category(name="Salary")
        row = category.to_sheet_row()
        assert isinstance(row, list)
        assert "salary" in row
