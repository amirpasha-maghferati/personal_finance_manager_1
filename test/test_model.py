from model.category import Category
from model.transaction import Transaction
from model.reminder import Reminder
from datetime import date


salary = Category(1, "Salary", "income")
salary.show_info()

print("----------------")

income = Transaction(
    1, 20000000, "income", 1, "Monthly salary"
)
income.show_info()

print("----------------")

reminder = Reminder(
    1, "Rent", 5000000, date(2026, 12, 17), 2
)

print(reminder.check_reminder())
reminder.show_info()
