from model.reminder import Reminder


class ReminderService:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, reminder):
        if not isinstance(reminder, Reminder):
            raise TypeError("Invalid reminder object")

        self.reminders.append(reminder)
        return reminder

    def get_all_reminders(self):
        return self.reminders

    def get_due_reminders(self):
        due_reminders = []

        for reminder in self.reminders:
            if reminder.check_reminder() == "Payment is due!":
                due_reminders.append(reminder)

        return due_reminders

    def mark_as_paid(self, reminder_id):
        for reminder in self.reminders:
            if reminder.reminder_id == reminder_id:
                reminder.mark_as_paid()
                return True

        return False










    def find_reminder(self, reminder_id):
        for reminder in self.reminders:
            if reminder.reminder_id == reminder_id:
                return reminder

        return None

    def delete_reminder(self, reminder_id):
        reminder = self.find_reminder(reminder_id)

        if reminder is None:
            return False

        self.reminders.remove(reminder)
        return True




