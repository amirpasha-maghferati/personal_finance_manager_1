from datetime import datetime
class Transaction:
    VALID_TYPES = ("income", "expense")
    def __init__(self, transaction_id, amount, transaction_type, category_id, description="", created_at=None):
        self.set_transaction_id(transaction_id); self.set_amount(amount); self.set_transaction_type(transaction_type)
        self.set_category_id(category_id); self.set_description(description)
        self.set_created_at(created_at if created_at is not None else datetime.now())
    def get_transaction_id(self): return self.__transaction_id
    def set_transaction_id(self, value):
        if value is None or str(value).strip() == "": raise ValueError("Transaction ID cannot be empty.")
        self.__transaction_id = value
    def get_amount(self): return self.__amount
    @property
    def amount(self):
        """Compatibility alias for older code that accesses transaction.amount."""
        return self.get_amount()
    @amount.setter
    def amount(self, value):
        self.set_amount(value)
    def set_amount(self, value):
        if isinstance(value, bool): raise ValueError("Amount must be positive.")
        try: value = float(value)
        except (TypeError, ValueError): raise ValueError("Amount must be a number.")
        if value <= 0: raise ValueError("Amount must be greater than zero.")
        self.__amount = value
    def get_transaction_type(self): return self.__transaction_type
    def set_transaction_type(self, value):
        if not isinstance(value, str): raise ValueError("Transaction type must be a string.")
        value = value.strip().lower()
        if value not in self.VALID_TYPES: raise ValueError("Type must be income or expense.")
        self.__transaction_type = value
    def get_category_id(self): return self.__category_id
    def set_category_id(self, value):
        if value is None or str(value).strip() == "": raise ValueError("Category ID cannot be empty.")
        self.__category_id = value
    @property
    def description(self):
        """Compatibility alias for older code that accesses transaction.description."""
        return self.get_description()
    @description.setter
    def description(self, value):
        self.set_description(value)
    def get_description(self): return self.__description
    def set_description(self, value):
        if value is None: value = ""
        if not isinstance(value, str): raise ValueError("Description must be a string.")
        self.__description = value.strip()
    def get_created_at(self): return self.__created_at
    def set_created_at(self, value):
        if not isinstance(value, datetime): raise ValueError("created_at must be datetime.")
        self.__created_at = value
    def get_signed_amount(self): return self.__amount if self.__transaction_type == "income" else -self.__amount
    def show_info(self):
        return f"Transaction(id={self.__transaction_id}, amount={self.__amount:.2f}, type='{self.__transaction_type}', category_id={self.__category_id}, description='{self.__description}')"
    def __str__(self): return self.show_info()
class Income(Transaction):
    def __init__(self, transaction_id, amount, category_id, description="", created_at=None):
        super().__init__(transaction_id, amount, "income", category_id, description, created_at)
    def get_signed_amount(self): return self.get_amount()
class Expense(Transaction):
    def __init__(self, transaction_id, amount, category_id, description="", created_at=None):
        super().__init__(transaction_id, amount, "expense", category_id, description, created_at)
    def get_signed_amount(self): return -self.get_amount()
