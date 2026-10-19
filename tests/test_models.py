import unittest
from datetime import date, datetime, timedelta

from model import Category, Transaction, Income, Expense, Reminder


class TestCategory(unittest.TestCase):
    def test_create_and_getters(self):
        category = Category(1, " Salary ", "INCOME")
        self.assertEqual(category.get_category_id(), 1)
        self.assertEqual(category.get_name(), "Salary")
        self.assertEqual(category.get_category_type(), "income")

    def test_setters(self):
        category = Category(1, "Salary", "income")
        category.set_name("Groceries")
        category.set_category_type("expense")
        self.assertEqual(category.get_name(), "Groceries")
        self.assertEqual(category.get_category_type(), "expense")

    def test_invalid_name_and_type(self):
        with self.assertRaises(ValueError):
            Category(1, "   ", "income")
        with self.assertRaises(ValueError):
            Category(2, "Other", "unknown")


class TestTransaction(unittest.TestCase):
    def test_create_and_getters(self):
        transaction = Transaction(1, 200000, "income", 10, "Monthly salary")
        self.assertEqual(transaction.get_transaction_id(), 1)
        self.assertEqual(transaction.get_amount(), 200000.0)
        self.assertEqual(transaction.get_transaction_type(), "income")
        self.assertEqual(transaction.get_category_id(), 10)
        self.assertEqual(transaction.get_description(), "Monthly salary")
        self.assertIsInstance(transaction.get_created_at(), datetime)

    def test_setters_and_signed_amount(self):
        transaction = Transaction(1, 500, "expense", 2)
        transaction.set_amount(700)
        transaction.set_description(" Groceries ")
        self.assertEqual(transaction.get_amount(), 700.0)
        self.assertEqual(transaction.get_description(), "Groceries")
        self.assertEqual(transaction.get_signed_amount(), -700.0)

    def test_invalid_amount_and_type(self):
        for amount in (0, -1, "abc", True):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    Transaction(1, amount, "income", 1)
        with self.assertRaises(ValueError):
            Transaction(1, 100, "transfer", 1)

    def test_income_and_expense_polymorphism(self):
        income = Income(1, 1000, 1, "Salary")
        expense = Expense(2, 250, 2, "Food")
        self.assertEqual(income.get_transaction_type(), "income")
        self.assertEqual(expense.get_transaction_type(), "expense")
        self.assertEqual(income.get_signed_amount(), 1000.0)
        self.assertEqual(expense.get_signed_amount(), -250.0)


class TestReminder(unittest.TestCase):
    def test_create_and_getters(self):
        reminder = Reminder(1, "Pay bill", "2026-12-01", 2, "Electricity")
        self.assertEqual(reminder.get_title(), "Pay bill")
        self.assertEqual(reminder.get_due_date(), date(2026, 12, 1))
        self.assertFalse(reminder.is_completed())

    def test_mark_completed_and_due(self):
        reminder = Reminder(1, "Pay bill", date.today() - timedelta(days=1), 2)
        self.assertTrue(reminder.is_due())
        reminder.mark_as_completed()
        self.assertTrue(reminder.is_completed())
        self.assertFalse(reminder.is_due())

    def test_setters_and_validation(self):
        reminder = Reminder(1, "Pay bill", date.today(), 2)
        reminder.set_title("Internet bill")
        reminder.set_notes(" Pay before deadline ")
        self.assertEqual(reminder.get_title(), "Internet bill")
        self.assertEqual(reminder.get_notes(), "Pay before deadline")
        with self.assertRaises(ValueError):
            reminder.set_due_date("not-a-date")
        with self.assertRaises(ValueError):
            reminder.set_completed("yes")


if __name__ == "__main__":
    unittest.main()
