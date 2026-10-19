from datetime import date


class Reminder:
    """Represents a reminder for a future payment or finance-related task."""

    def __init__(self, reminder_id, title, due_date, category_id,
                 notes="", completed=False):
        self.set_reminder_id(reminder_id)
        self.set_title(title)
        self.set_due_date(due_date)
        self.set_category_id(category_id)
        self.set_notes(notes)
        self.set_completed(completed)

    def get_reminder_id(self):
        return self.__reminder_id

    def set_reminder_id(self, reminder_id):
        if reminder_id is None or str(reminder_id).strip() == "":
            raise ValueError("Reminder ID cannot be empty.")
        self.__reminder_id = reminder_id

    def get_title(self):
        return self.__title

    def set_title(self, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Reminder title cannot be empty.")
        self.__title = title.strip()

    def get_due_date(self):
        return self.__due_date

    def set_due_date(self, due_date):
        if isinstance(due_date, str):
            try:
                due_date = date.fromisoformat(due_date)
            except ValueError:
                raise ValueError("Date must use YYYY-MM-DD format.")
        if not isinstance(due_date, date):
            raise ValueError("due_date must be a date object or YYYY-MM-DD string.")
        self.__due_date = due_date

    def get_category_id(self):
        return self.__category_id

    def set_category_id(self, category_id):
        if category_id is None or str(category_id).strip() == "":
            raise ValueError("Category ID cannot be empty.")
        self.__category_id = category_id

    def get_notes(self):
        return self.__notes

    def set_notes(self, notes):
        if notes is None:
            notes = ""
        if not isinstance(notes, str):
            raise ValueError("Notes must be a string.")
        self.__notes = notes.strip()

    def is_completed(self):
        return self.__completed

    def set_completed(self, completed):
        if not isinstance(completed, bool):
            raise ValueError("completed must be True or False.")
        self.__completed = completed

    def mark_as_completed(self):
        self.__completed = True

    def is_due(self, today=None):
        if self.__completed:
            return False
        if today is None:
            today = date.today()
        if not isinstance(today, date):
            raise ValueError("today must be a date object.")
        return self.__due_date <= today

    def show_info(self):
        status = "completed" if self.__completed else "pending"
        return (
            f"Reminder(id={self.__reminder_id}, title='{self.__title}', "
            f"due_date={self.__due_date.isoformat()}, status='{status}')"
        )

    def __str__(self):
        return self.show_info()
