from model.transaction import Transaction


class TransactionService:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError("Invalid transaction object")

        self.transactions.append(transaction)
        return transaction

    def get_all_transactions(self):
        return self.transactions

    def find_transaction(self, transaction_id):
        for transaction in self.transactions:
            if transaction.transaction_id == transaction_id:
                return transaction

        return None

    def delete_transaction(self, transaction_id):
        transaction = self.find_transaction(transaction_id)

        if transaction is None:
            return False

        self.transactions.remove(transaction)
        return True

    def calculate_balance(self):
        balance = 0

        for transaction in self.transactions:
            if transaction.transaction_type == "income":
                balance += transaction.amount
            elif transaction.transaction_type == "expense":
                balance -= transaction.amount

        return balance









    def update_transaction(
        self,
        transaction_id,
        new_amount,
        new_type,
        new_category_id,
        new_description
    ):
        transaction = self.find_transaction(transaction_id)

        if transaction is None:
            return False

        if float(new_amount) <= 0:
            raise ValueError("Amount must be positive!")

        if new_type not in ["income", "expense"]:
            raise ValueError("Invalid transaction type!")

        transaction.amount = float(new_amount)
        transaction.transaction_type = new_type
        transaction.category_id = new_category_id
        transaction.description = new_description

        return True

