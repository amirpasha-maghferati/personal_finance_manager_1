
class Category:
    def __init__(self, category_id, name, category_type):
        self.category_id = category_id
        self.name = name
        self.category_type = category_type

    def show_info(self):
        print("ID:", self.category_id)
        print("Name:", self.name)
        print("Type:", self.category_type)

    def change_name(self, new_name):
        if new_name.strip() != "":
            self.name = new_name
        else:
            print("Name cannot be empty!")
