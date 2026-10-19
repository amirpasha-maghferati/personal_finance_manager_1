from service.transaction_service import TransactionService

class TransactionController:
    def __init__(self, service=None):
        self.__service = service if service is not None else TransactionService()

    def add_transaction(self, transaction):
        return self.__service.add_transaction(transaction)

    def get_all_transactions(self):
        return self.__service.get_all_transactions()

    def find_transaction(self, transaction_id):
        return self.__service.find_transaction(transaction_id)

    def delete_transaction(self, transaction_id):
        return self.__service.delete_transaction(transaction_id)

    def update_transaction(self, transaction_id, **changes):
        return self.__service.update_transaction(transaction_id, **changes)

    def get_balance(self):
        return self.__service.calculate_balance()

    def get_total_income(self):
        return self.__service.calculate_total_income()

    def get_total_expenses(self):
        return self.__service.calculate_total_expenses()
