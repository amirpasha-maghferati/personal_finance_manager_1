
from controller.transaction_controller import TransactionController

controller = TransactionController()

controller.create_transaction(
    1, 20000000, "income", "1", "حقوق"
)

controller.create_transaction(
    2, 2000000, "expense", "2", "خرید مایحتاج"
)

print("Balance:", controller.get_balance())

for transaction in controller.get_transactions():
    transaction.show_info()
