from model.transaction import Transaction, Income, Expense


class TransactionService:
    def __init__(self):
        self.__transactions = []

    def add_transaction(self, item):
        if not isinstance(item, Transaction):
            raise TypeError("Expected Transaction, Income, or Expense.")
        if self.find_transaction(item.get_transaction_id()) is not None:
            raise ValueError("Duplicate transaction ID.")
        self.__transactions.append(item)
        return item

    def get_all_transactions(self):
        return list(self.__transactions)

    def find_transaction(self, item_id):
        for item in self.__transactions:
            if item.get_transaction_id() == item_id:
                return item
        return None

    def search_transactions(
        self, search_text="", transaction_type="all", category_id=None,
        sort_by="date", descending=True
    ):
        """Return filtered transactions without changing the stored list.

        search_text matches the description or transaction ID.
        transaction_type: all, income, or expense.
        category_id=None means all categories.
        sort_by: date, amount, or type.
        """
        text = str(search_text or "").strip().casefold()
        kind = str(transaction_type or "all").strip().casefold()
        if kind not in ("all", "income", "expense"):
            raise ValueError("transaction_type must be all, income, or expense.")
        if sort_by not in ("date", "amount", "type"):
            raise ValueError("sort_by must be date, amount, or type.")

        results = []
        for item in self.__transactions:
            if kind != "all" and item.get_transaction_type() != kind:
                continue
            if category_id not in (None, "", "all"):
                if str(item.get_category_id()) != str(category_id):
                    continue
            if text:
                description = str(item.get_description() or "").casefold()
                item_id = str(item.get_transaction_id()).casefold()
                if text not in description and text not in item_id:
                    continue
            results.append(item)

        if sort_by == "amount":
            key = lambda item: float(item.get_amount())
        elif sort_by == "type":
            key = lambda item: str(item.get_transaction_type()).casefold()
        else:
            key = lambda item: self._date_sort_key(item.get_created_at())

        return sorted(results, key=key, reverse=bool(descending))

    @staticmethod
    def _date_sort_key(value):
        """Make common datetime/date/string date values sortable."""
        if value is None:
            return ""
        if hasattr(value, "isoformat"):
            return value.isoformat()
        return str(value)

    def delete_transaction(self, item_id):
        item = self.find_transaction(item_id)
        if item is None:
            return False
        self.__transactions.remove(item)
        return True

    def update_transaction(self, item_id, amount=None, transaction_type=None,
                           category_id=None, description=None):
        item = self.find_transaction(item_id)
        if item is None:
            return False
        new_amount = item.get_amount() if amount is None else amount
        new_type = item.get_transaction_type() if transaction_type is None else transaction_type
        new_category = item.get_category_id() if category_id is None else category_id
        new_description = item.get_description() if description is None else description
        if new_type == "income":
            updated = Income(item_id, new_amount, new_category, new_description, item.get_created_at())
        elif new_type == "expense":
            updated = Expense(item_id, new_amount, new_category, new_description, item.get_created_at())
        else:
            raise ValueError("Type must be income or expense.")
        index = self.__transactions.index(item)
        self.__transactions[index] = updated
        return True

    def calculate_balance(self):
        return sum(item.get_signed_amount() for item in self.__transactions)

    def calculate_total_income(self):
        return sum(item.get_amount() for item in self.__transactions
                   if item.get_transaction_type() == "income")

    def calculate_total_expenses(self):
        return sum(item.get_amount() for item in self.__transactions
                   if item.get_transaction_type() == "expense")
