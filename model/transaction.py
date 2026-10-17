from datetime import datetime


class Transaction:
    def __init__(
        self,
        transaction_id,
        amount,
        transaction_type,
        category_id,
        description=""
    ):
        self.transaction_id = transaction_id
        self.amount = float(amount)
        self.transaction_type = transaction_type
        self.category_id = category_id
        self.description = description
        self.created_at = datetime.now()

        if self.amount <= 0:
            raise ValueError("Amount must be positive!")

        if transaction_type not in ["income", "expense"]:
            raise ValueError("Invalid transaction type!")

    def show_info(self):
        print("ID:", self.transaction_id)
        print("Amount:", self.amount)
        print("Type:", self.transaction_type)
        print("Category ID:", self.category_id)
        print("Description:", self.description)
        print("Date:", self.created_at)

    def change_description(self, new_description):
        self.description = new_description
