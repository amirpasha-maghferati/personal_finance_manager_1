from datetime import datetime


class Reminder:
    def __init__(
        self,
        reminder_id,
        title,
        amount,
        due_date,
        category_id
    ):
        self.reminder_id = reminder_id
        self.title = title
        self.amount = float(amount)
        self.due_date = due_date
        self.category_id = category_id
        self.is_paid = False

    def mark_as_paid(self):
        self.is_paid = True

    def check_reminder(self):
        today = datetime.now().date()

        if self.is_paid:
            return "This payment is already paid."

        if self.due_date <= today:
            return "Payment is due!"

        return "Payment is not due yet."

    def show_info(self):
        print("Title:", self.title)
        print("Amount:", self.amount)
        print("Due date:", self.due_date)
        print("Paid:", self.is_paid)
