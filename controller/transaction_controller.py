"""Transaction controller with compatibility aliases for older code."""
from model.transaction import Income, Expense, Transaction
from service.transaction_service import TransactionService


class TransactionController:
    def __init__(self, service=None):
        self.__service = service if service is not None else TransactionService()

    @property
    def service(self):
        """Backward-compatible access for older tests/code."""
        return self.__service

    def add_transaction(self, item):
        return self.__service.add_transaction(item)

    def create_transaction(self, transaction_id, amount=None, transaction_type=None,
                           category_id=None, description="", created_at=None):
        if isinstance(transaction_id, Transaction):
            return self.add_transaction(transaction_id)
        kind = str(transaction_type).strip().lower() if transaction_type is not None else ""
        if kind == "income":
            item = Income(transaction_id, amount, category_id, description, created_at)
        elif kind == "expense":
            item = Expense(transaction_id, amount, category_id, description, created_at)
        else:
            raise ValueError("transaction_type must be 'income' or 'expense'.")
        return self.add_transaction(item)

    def get_all_transactions(self):
        return self.__service.get_all_transactions()

    def get_transactions(self):
        return self.get_all_transactions()

    def search_transactions(self, search_text="", transaction_type="all",
                            category_id=None, sort_by="date", descending=True):
        return self.__service.search_transactions(
            search_text=search_text,
            transaction_type=transaction_type,
            category_id=category_id,
            sort_by=sort_by,
            descending=descending,
        )

    def find_transaction(self, item_id):
        return self.__service.find_transaction(item_id)

    def delete_transaction(self, item_id):
        return self.__service.delete_transaction(item_id)

    def update_transaction(self, item_id, amount=None, transaction_type=None,
                           category_id=None, description=None, **changes):
        if amount is not None:
            changes["amount"] = amount
        if transaction_type is not None:
            changes["transaction_type"] = transaction_type
        if category_id is not None:
            changes["category_id"] = category_id
        if description is not None:
            changes["description"] = description
        return self.__service.update_transaction(item_id, **changes)

    def get_balance(self):
        return self.__service.calculate_balance()

    def get_total_income(self):
        return self.__service.calculate_total_income()

    def get_total_expenses(self):
        return self.__service.calculate_total_expenses()
