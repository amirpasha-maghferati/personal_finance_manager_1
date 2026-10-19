"""Reminder controller supporting both current and legacy method names."""
from datetime import date
from model.reminder import Reminder
from service.reminder_service import ReminderService


class ReminderController:
    def __init__(self, service=None):
        self.__service = service if service is not None else ReminderService()

    def add_reminder(self, item):
        return self.__service.add_reminder(item)

    def create_reminder(self, reminder_id, title=None, amount_or_due_date=None,
                        due_date_or_category=None, category_id=None, notes="", completed=False):
        """Accept a Reminder object or legacy fields (id, title, amount, due_date, category_id)."""
        if isinstance(reminder_id, Reminder):
            return self.add_reminder(reminder_id)

        # Legacy tests pass: id, title, amount, date, category_id.
        if isinstance(due_date_or_category, date):
            item = Reminder(
                reminder_id, title, amount_or_due_date,
                due_date_or_category, category_id
            )
        else:
            # Current signature: id, title, due_date, category_id, notes, completed
            actual_due_date = amount_or_due_date
            actual_category_id = due_date_or_category
            item = Reminder(reminder_id, title, actual_due_date,
                            actual_category_id, notes, completed)
        return self.add_reminder(item)

    def get_all_reminders(self):
        return self.__service.get_all_reminders()

    def get_reminders(self):
        return self.get_all_reminders()

    def find_reminder(self, item_id):
        return self.__service.find_reminder(item_id)

    def get_due_reminders(self, today=None):
        return self.__service.get_due_reminders(today)

    def mark_as_completed(self, item_id):
        return self.__service.mark_as_completed(item_id)

    def mark_as_paid(self, item_id):
        return self.__service.mark_as_completed(item_id)

    def delete_reminder(self, item_id):
        return self.__service.delete_reminder(item_id)
