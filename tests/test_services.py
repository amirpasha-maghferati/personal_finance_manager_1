import unittest
from datetime import date, timedelta
from model import Category, Transaction, Income, Expense, Reminder
from service import TransactionService, CategoryService, ReminderService
from controller import TransactionController, CategoryController, ReminderController

class TestTransactionService(unittest.TestCase):
    def setUp(self):
        self.service = TransactionService()
        self.service.add_transaction(Income(1, 200000, 1, "Salary"))
        self.service.add_transaction(Expense(2, 25000, 2, "Groceries"))

    def test_totals_and_balance(self):
        self.assertEqual(self.service.calculate_total_income(), 200000)
        self.assertEqual(self.service.calculate_total_expenses(), 25000)
        self.assertEqual(self.service.calculate_balance(), 175000)

    def test_find_delete_and_missing(self):
        self.assertIsNotNone(self.service.find_transaction(1))
        self.assertTrue(self.service.delete_transaction(2))
        self.assertFalse(self.service.delete_transaction(999))
        self.assertEqual(self.service.calculate_balance(), 200000)

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            self.service.add_transaction(Transaction(1, 10, "expense", 2))

    def test_update_and_invalid_update_is_safe(self):
        self.assertTrue(self.service.update_transaction(2, amount=30000, description="Transport"))
        self.assertEqual(self.service.calculate_balance(), 170000)
        with self.assertRaises(ValueError):
            self.service.update_transaction(2, amount=-5)
        self.assertEqual(self.service.find_transaction(2).get_amount(), 30000)

    def test_get_all_returns_copy_of_list(self):
        result = self.service.get_all_transactions()
        result.clear()
        self.assertEqual(len(self.service.get_all_transactions()), 2)

class TestCategoryService(unittest.TestCase):
    def setUp(self):
        self.service = CategoryService()
        self.service.add_category(Category(1, "Salary", "income"))
        self.service.add_category(Category(2, "Groceries", "expense"))

    def test_add_find_update_delete(self):
        self.assertEqual(self.service.find_category(1).get_name(), "Salary")
        self.assertTrue(self.service.update_category(2, name="Food"))
        self.assertEqual(self.service.find_category(2).get_name(), "Food")
        with self.assertRaises(ValueError):
            self.service.update_category(2, name=" ")
        self.assertEqual(self.service.find_category(2).get_name(), "Food")
        self.assertTrue(self.service.delete_category(1))
        self.assertFalse(self.service.delete_category(1))

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            self.service.add_category(Category(1, "Other", "both"))

class TestReminderService(unittest.TestCase):
    def setUp(self):
        self.service = ReminderService()
        self.service.add_reminder(Reminder(1, "Electricity", date.today() - timedelta(days=1), 2))
        self.service.add_reminder(Reminder(2, "Internet", date.today() + timedelta(days=10), 2))

    def test_due_reminders(self):
        self.assertEqual([r.get_reminder_id() for r in self.service.get_due_reminders()], [1])

    def test_complete_and_delete(self):
        self.assertTrue(self.service.mark_as_completed(1))
        self.assertEqual(self.service.get_due_reminders(), [])
        self.assertTrue(self.service.delete_reminder(2))
        self.assertFalse(self.service.delete_reminder(2))

    def test_duplicate_id(self):
        with self.assertRaises(ValueError):
            self.service.add_reminder(Reminder(1, "Duplicate", date.today(), 2))

class TestControllers(unittest.TestCase):
    def test_transaction_controller(self):
        controller = TransactionController()
        controller.add_transaction(Income(1, 1000, 1))
        controller.add_transaction(Expense(2, 300, 2))
        self.assertEqual(controller.get_balance(), 700)
        self.assertEqual(controller.get_total_income(), 1000)
        self.assertEqual(controller.get_total_expenses(), 300)

    def test_category_controller(self):
        controller = CategoryController()
        controller.add_category(Category(1, "Salary", "income"))
        self.assertEqual(len(controller.get_all_categories()), 1)

    def test_reminder_controller(self):
        controller = ReminderController()
        controller.add_reminder(Reminder(1, "Bill", date.today(), 2))
        self.assertEqual(len(controller.get_due_reminders()), 1)
        self.assertTrue(controller.mark_as_completed(1))
        self.assertEqual(len(controller.get_due_reminders()), 0)

if __name__ == "__main__":
    unittest.main()
