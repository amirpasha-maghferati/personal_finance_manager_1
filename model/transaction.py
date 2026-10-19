from datetime import datetime


class Transaction:
    """Base transaction model. Amount is always stored as a positive number."""

    VALID_TYPES = ("income", "expense")

    def __init__(self, transaction_id, amount, transaction_type, category_id,
                 description="", created_at=None):
        self.set_transaction_id(transaction_id)
        self.set_amount(amount)
        self.set_transaction_type(transaction_type)
        self.set_category_id(category_id)
        self.set_description(description)
        self.set_created_at(created_at if created_at is not None else datetime.now())

    def get_transaction_id(self):
        return self.__transaction_id

    def set_transaction_id(self, transaction_id):
        if transaction_id is None or str(transaction_id).strip() == "":
            raise ValueError("Transaction ID cannot be empty.")
        self.__transaction_id = transaction_id

    def get_amount(self):
        return self.__amount

    def set_amount(self, amount):
        if isinstance(amount, bool):
            raise ValueError("Amount must be a positive number.")
        try:
            amount = float(amount)
        except (TypeError, ValueError):
            raise ValueError("Amount must be a number.")
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        self.__amount = amount

    def get_transaction_type(self):
        return self.__transaction_type

    def set_transaction_type(self, transaction_type):
        if not isinstance(transaction_type, str):
            raise ValueError("Transaction type must be a string.")
        transaction_type = transaction_type.strip().lower()
        if transaction_type not in self.VALID_TYPES:
            raise ValueError("Transaction type must be income or expense.")
        self.__transaction_type = transaction_type

    def get_category_id(self):
        return self.__category_id

    def set_category_id(self, category_id):
        if category_id is None or str(category_id).strip() == "":
            raise ValueError("Category ID cannot be empty.")
        self.__category_id = category_id

    def get_description(self):
        return self.__description

    def set_description(self, description):
        if description is None:
            description = ""
        if not isinstance(description, str):
            raise ValueError("Description must be a string.")
        self.__description = description.strip()

    def get_created_at(self):
        return self.__created_at

    def set_created_at(self, created_at):
        if not isinstance(created_at, datetime):
            raise ValueError("created_at must be a datetime object.")
        self.__created_at = created_at

    def get_signed_amount(self):
        if self.__transaction_type == "income":
            return self.__amount
        return -self.__amount

    def show_info(self):
        return (
            f"Transaction(id={self.__transaction_id}, amount={self.__amount:.2f}, "
            f"type='{self.__transaction_type}', category_id={self.__category_id}, "
            f"description='{self.__description}')"
        )

    def __str__(self):
        return self.show_info()


class Income(Transaction):
    """Specialized income transaction; demonstrates inheritance/polymorphism."""

    def __init__(self, transaction_id, amount, category_id, description="", created_at=None):
        super().__init__(transaction_id, amount, "income", category_id, description, created_at)

    def get_signed_amount(self):
        return self.get_amount()


class Expense(Transaction):
    """Specialized expense transaction; demonstrates inheritance/polymorphism."""

    def __init__(self, transaction_id, amount, category_id, description="", created_at=None):
        super().__init__(transaction_id, amount, "expense", category_id, description, created_at)

    def get_signed_amount(self):
        return -self.get_amount()
