from model.transaction import Transaction

class TransactionService:
    def __init__(self):
        self.__transactions = []

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError("transaction must be a Transaction, Income, or Expense object.")
        if self.find_transaction(transaction.get_transaction_id()) is not None:
            raise ValueError("A transaction with this ID already exists.")
        self.__transactions.append(transaction)
        return transaction

    def get_all_transactions(self):
        return list(self.__transactions)

    def find_transaction(self, transaction_id):
        for transaction in self.__transactions:
            if transaction.get_transaction_id() == transaction_id:
                return transaction
        return None

    def delete_transaction(self, transaction_id):
        transaction = self.find_transaction(transaction_id)
        if transaction is None:
            return False
        self.__transactions.remove(transaction)
        return True

    def update_transaction(self, transaction_id, amount=None, transaction_type=None,
                           category_id=None, description=None):
        transaction = self.find_transaction(transaction_id)
        if transaction is None:
            return False
        # Validate every requested field before mutating the original object.
        checked = Transaction(
            transaction_id,
            transaction.get_amount() if amount is None else amount,
            transaction.get_transaction_type() if transaction_type is None else transaction_type,
            transaction.get_category_id() if category_id is None else category_id,
            transaction.get_description() if description is None else description,
            transaction.get_created_at()
        )
        transaction.set_amount(checked.get_amount())
        transaction.set_transaction_type(checked.get_transaction_type())
        transaction.set_category_id(checked.get_category_id())
        transaction.set_description(checked.get_description())
        return True

    def calculate_balance(self):
        return sum(item.get_signed_amount() for item in self.__transactions)

    def calculate_total_income(self):
        return sum(item.get_amount() for item in self.__transactions
                   if item.get_transaction_type() == "income")

    def calculate_total_expenses(self):
        return sum(item.get_amount() for item in self.__transactions
                   if item.get_transaction_type() == "expense")
