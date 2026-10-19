"""Reminder model with current fields and compatibility for legacy payment reminders."""
from datetime import date, datetime


class Reminder:
    def __init__(self, reminder_id, title, due_date, category_id, notes="", completed=False):
        # Legacy constructor: Reminder(id, title, amount, due_date, category_id)
        # In that form the third argument is an amount and the fourth is a date.
        self.__amount = None
        self.__paid = False
        if isinstance(category_id, (date, datetime)) and isinstance(due_date, (int, float)):
            amount = due_date
            actual_due_date = category_id
            actual_category_id = notes
            actual_notes = ""
            self.set_amount(amount)
            due_date = actual_due_date
            category_id = actual_category_id
            notes = actual_notes
        self.set_reminder_id(reminder_id)
        self.set_title(title)
        self.set_due_date(due_date)
        self.set_category_id(category_id)
        self.set_notes(notes)
        self.set_completed(completed)

    def get_reminder_id(self): return self.__reminder_id
    def set_reminder_id(self, value):
        if value is None or str(value).strip() == "":
            raise ValueError("Reminder ID cannot be empty.")
        self.__reminder_id = value

    def get_title(self): return self.__title
    def set_title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Reminder title cannot be empty.")
        self.__title = value.strip()

    def get_due_date(self): return self.__due_date
    def set_due_date(self, value):
        if isinstance(value, datetime):
            value = value.date()
        elif isinstance(value, str):
            raw = value.strip()
            parsed = None
            for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
                try:
                    parsed = datetime.strptime(raw, fmt).date()
                    break
                except ValueError:
                    pass
            if parsed is None:
                try: parsed = date.fromisoformat(raw)
                except ValueError as exc:
                    raise ValueError("Date must use YYYY-MM-DD or a common date format.") from exc
            value = parsed
        if not isinstance(value, date):
            raise ValueError("due_date must be a date object or date string.")
        self.__due_date = value

    def get_category_id(self): return self.__category_id
    def set_category_id(self, value):
        if value is None or str(value).strip() == "":
            raise ValueError("Category ID cannot be empty.")
        self.__category_id = value

    def get_notes(self): return self.__notes
    def set_notes(self, value):
        if value is None: value = ""
        if not isinstance(value, str): raise ValueError("Notes must be a string.")
        self.__notes = value.strip()

    def set_amount(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Amount must be a non-negative number.")
        self.__amount = value
    def get_amount(self): return self.__amount

    @property
    def is_paid(self): return self.__paid
    @is_paid.setter
    def is_paid(self, value):
        if not isinstance(value, bool): raise ValueError("is_paid must be boolean.")
        self.__paid = value
        if value: self.__completed = True

    def is_completed(self): return self.__completed
    def set_completed(self, value):
        if not isinstance(value, bool): raise ValueError("completed must be boolean.")
        self.__completed = value
        self.__paid = value

    def mark_as_completed(self):
        self.__completed = True
        self.__paid = True

    def mark_as_paid(self):
        self.mark_as_completed()

    def is_due(self, today=None):
        if self.__completed: return False
        if today is None: today = date.today()
        elif isinstance(today, datetime): today = today.date()
        if not isinstance(today, date): raise ValueError("today must be a date object.")
        return self.__due_date <= today

    def show_info(self):
        status = "completed" if self.__completed else "pending"
        return f"Reminder(id={self.__reminder_id}, title='{self.__title}', due_date={self.__due_date.isoformat()}, status='{status}')"
    def __str__(self): return self.show_info()
