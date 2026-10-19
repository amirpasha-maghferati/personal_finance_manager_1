class Category:
    """Represents a transaction category, such as Salary or Groceries."""

    VALID_TYPES = ("income", "expense", "both")

    def __init__(self, category_id, name, category_type):
        self.set_category_id(category_id)
        self.set_name(name)
        self.set_category_type(category_type)

    def get_category_id(self):
        return self.__category_id

    def set_category_id(self, category_id):
        if category_id is None or str(category_id).strip() == "":
            raise ValueError("Category ID cannot be empty.")
        self.__category_id = category_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Category name cannot be empty.")
        self.__name = name.strip()

    def get_category_type(self):
        return self.__category_type

    def set_category_type(self, category_type):
        if not isinstance(category_type, str):
            raise ValueError("Category type must be a string.")
        category_type = category_type.strip().lower()
        if category_type not in self.VALID_TYPES:
            raise ValueError("Category type must be income, expense, or both.")
        self.__category_type = category_type

    def show_info(self):
        return f"Category(id={self.__category_id}, name='{self.__name}', type='{self.__category_type}')"

    def __str__(self):
        return self.show_info()
