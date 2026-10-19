import unittest
from model.transaction import Income, Expense
from service.transaction_service import TransactionService


class TransactionEditDeleteTests(unittest.TestCase):
    def setUp(self):
        self.service = TransactionService()
        self.service.add_transaction(Income(1, 1000, 1, "حقوق"))

    def test_update_income_to_expense_updates_balance(self):
        self.assertTrue(self.service.update_transaction(1, amount=250, transaction_type="expense", category_id=2, description="خرید"))
        updated = self.service.find_transaction(1)
        self.assertIsInstance(updated, Expense)
        self.assertEqual(updated.get_amount(), 250)
        self.assertEqual(self.service.calculate_balance(), -250)

    def test_delete_transaction_updates_totals(self):
        self.assertTrue(self.service.delete_transaction(1))
        self.assertEqual(self.service.calculate_balance(), 0)
        self.assertEqual(self.service.calculate_total_income(), 0)

    def test_invalid_amount_does_not_replace_transaction(self):
        with self.assertRaises(ValueError):
            self.service.update_transaction(1, amount=-5)
        self.assertEqual(self.service.calculate_balance(), 1000)


if __name__ == "__main__":
    unittest.main()
