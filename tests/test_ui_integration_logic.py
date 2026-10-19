import unittest
from model import Income, Expense
from controller import TransactionController

class TestUIIntegrationLogic(unittest.TestCase):
    def test_controller_updates_dashboard_values(self):
        controller = TransactionController()
        controller.add_transaction(Income(1, 200000, 1, "حقوق"))
        controller.add_transaction(Expense(2, 25000, 2, "خرید مایحتاج"))
        self.assertEqual(controller.get_balance(), 175000)
        self.assertEqual(controller.get_total_income(), 200000)
        self.assertEqual(controller.get_total_expenses(), 25000)

    def test_invalid_transaction_does_not_change_balance(self):
        controller = TransactionController()
        controller.add_transaction(Income(1, 1000, 1))
        with self.assertRaises(ValueError):
            controller.add_transaction(Expense(2, -5, 2))
        self.assertEqual(controller.get_balance(), 1000)

if __name__ == "__main__":
    unittest.main()
