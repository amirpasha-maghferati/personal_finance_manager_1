from service.reminder_service import ReminderService
from model.reminder import Reminder


class ReminderController:
    def __init__(self):
        self.service = ReminderService()

    def create_reminder(
        self,
        reminder_id,
        title,
        amount,
        due_date,
        category_id
    ):
        reminder = Reminder(
            reminder_id,
            title,
            amount,
            due_date,
            category_id
        )

        return self.service.add_reminder(reminder)

    def get_reminders(self):
        return self.service.get_all_reminders()

    def get_due_reminders(self):
        return self.service.get_due_reminders()

    def mark_as_paid(self, reminder_id):
        return self.service.mark_as_paid(reminder_id)









    def delete_reminder(self, reminder_id):
        return self.service.delete_reminder(reminder_id)

    def find_reminder(self, reminder_id):
        return self.service.find_reminder(reminder_id)

