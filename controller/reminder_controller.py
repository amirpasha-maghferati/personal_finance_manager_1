from service.reminder_service import ReminderService

class ReminderController:
    def __init__(self, service=None):
        self.__service = service if service is not None else ReminderService()

    def add_reminder(self, reminder):
        return self.__service.add_reminder(reminder)

    def get_all_reminders(self):
        return self.__service.get_all_reminders()

    def find_reminder(self, reminder_id):
        return self.__service.find_reminder(reminder_id)

    def get_due_reminders(self, today=None):
        return self.__service.get_due_reminders(today)

    def mark_as_completed(self, reminder_id):
        return self.__service.mark_as_completed(reminder_id)

    def delete_reminder(self, reminder_id):
        return self.__service.delete_reminder(reminder_id)
