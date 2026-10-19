from model.reminder import Reminder

class ReminderService:
    def __init__(self):
        self.__reminders = []

    def add_reminder(self, reminder):
        if not isinstance(reminder, Reminder):
            raise TypeError("reminder must be a Reminder object.")
        if self.find_reminder(reminder.get_reminder_id()) is not None:
            raise ValueError("A reminder with this ID already exists.")
        self.__reminders.append(reminder)
        return reminder

    def get_all_reminders(self):
        return list(self.__reminders)

    def find_reminder(self, reminder_id):
        for reminder in self.__reminders:
            if reminder.get_reminder_id() == reminder_id:
                return reminder
        return None

    def get_due_reminders(self, today=None):
        return [item for item in self.__reminders if item.is_due(today)]

    def mark_as_completed(self, reminder_id):
        reminder = self.find_reminder(reminder_id)
        if reminder is None:
            return False
        reminder.mark_as_completed()
        return True

    # Backward-compatible alias for older code that calls reminders "paid".
    def mark_as_paid(self, reminder_id):
        return self.mark_as_completed(reminder_id)

    def delete_reminder(self, reminder_id):
        reminder = self.find_reminder(reminder_id)
        if reminder is None:
            return False
        self.__reminders.remove(reminder)
        return True
