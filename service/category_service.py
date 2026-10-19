from model.category import Category

class CategoryService:
    def __init__(self):
        self.__categories = []

    def add_category(self, category):
        if not isinstance(category, Category):
            raise TypeError("category must be a Category object.")
        if self.find_category(category.get_category_id()) is not None:
            raise ValueError("A category with this ID already exists.")
        self.__categories.append(category)
        return category

    def get_all_categories(self):
        return list(self.__categories)

    def find_category(self, category_id):
        for category in self.__categories:
            if category.get_category_id() == category_id:
                return category
        return None

    def update_category(self, category_id, name=None, category_type=None):
        category = self.find_category(category_id)
        if category is None:
            return False
        checked = Category(category_id,
                           category.get_name() if name is None else name,
                           category.get_category_type() if category_type is None else category_type)
        category.set_name(checked.get_name())
        category.set_category_type(checked.get_category_type())
        return True

    def delete_category(self, category_id):
        category = self.find_category(category_id)
        if category is None:
            return False
        self.__categories.remove(category)
        return True
