from service.category_service import CategoryService

class CategoryController:
    def __init__(self, service=None):
        self.__service = service if service is not None else CategoryService()

    def add_category(self, category):
        return self.__service.add_category(category)

    def get_all_categories(self):
        return self.__service.get_all_categories()

    def find_category(self, category_id):
        return self.__service.find_category(category_id)

    def update_category(self, category_id, **changes):
        return self.__service.update_category(category_id, **changes)

    def delete_category(self, category_id):
        return self.__service.delete_category(category_id)
