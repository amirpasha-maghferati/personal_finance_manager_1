from service.transaction_service import TransactionService
from model.transaction import Transaction


class TransactionController:
    def __init__(self):
        self.service = TransactionService()

    def create_transaction(
        self,
        transaction_id,
        amount,
        transaction_type,
        category_id,
        description=""
    ):
        transaction = Transaction(
            transaction_id,
            amount,
            transaction_type,
            category_id,
            description
        )

        return self.service.add_transaction(transaction)

    def get_transactions(self):
        return self.service.get_all_transactions()

    def get_balance(self):
        return self.service.calculate_balance()

    def delete_transaction(self, transaction_id):
        return self.service.delete_transaction(transaction_id)











    def update_transaction(
        self,
        transaction_id,
        new_amount,
        new_type,
        new_category_id,
        new_description
    ):
        return self.service.update_transaction(
            transaction_id,
            new_amount,
            new_type,
            new_category_id,
            new_description
        )

