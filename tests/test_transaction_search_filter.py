import unittest

from model import Income, Expense
from service.transaction_service import TransactionService


class TransactionSearchFilterTests(unittest.TestCase):
    def setUp(self):
        self.service = TransactionService()
        self.service.add_transaction(Income(1, 250000, 1, "حقوق ماهانه"))
        self.service.add_transaction(Expense(2, 45000, 2, "خرید نان و شیر"))
        self.service.add_transaction(Expense(3, 120000, 3, "تاکسی"))

    def test_search_by_description(self):
        results = self.service.search_transactions(search_text="نان")
        self.assertEqual([str(x.get_transaction_id()) for x in results], ["2"])

    def test_search_by_transaction_id(self):
        results = self.service.search_transactions(search_text="3")
        self.assertEqual([str(x.get_transaction_id()) for x in results], ["3"])

    def test_filter_by_type(self):
        results = self.service.search_transactions(transaction_type="expense")
        self.assertEqual(len(results), 2)
        self.assertTrue(all(x.get_transaction_type() == "expense" for x in results))

    def test_filter_by_category_id(self):
        results = self.service.search_transactions(category_id=2)
        self.assertEqual(len(results), 1)
        self.assertEqual(str(results[0].get_transaction_id()), "2")

    def test_sort_by_amount_descending(self):
        results = self.service.search_transactions(sort_by="amount", descending=True)
        amounts = [x.get_amount() for x in results]
        self.assertEqual(amounts, sorted(amounts, reverse=True))

    def test_search_does_not_change_original_transactions(self):
        before = list(self.service.get_all_transactions())
        self.service.search_transactions(search_text="نان", transaction_type="expense")
        after = self.service.get_all_transactions()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
