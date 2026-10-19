
from datetime import date, timedelta

from model.reminder import Reminder
from service.reminder_service import ReminderService


def test_add_reminder():
    service = ReminderService()

    reminder = Reminder(
        1,
        "پرداخت اجاره",
        5000000,
        date.today() + timedelta(days=30),
        "2"
    )

    service.add_reminder(reminder)

    assert len(service.get_all_reminders()) == 1
    print("Add reminder: PASS")


def test_due_reminders():
    service = ReminderService()

    reminder = Reminder(
        2,
        "پرداخت قبض",
        200000,
        date.today() - timedelta(days=1),
        "2"
    )

    service.add_reminder(reminder)

    due_reminders = service.get_due_reminders()

    assert len(due_reminders) == 1
    print("Due reminders: PASS")


def test_mark_as_paid():
    service = ReminderService()

    reminder = Reminder(
        3,
        "پرداخت قسط",
        1000000,
        date.today(),
        "2"
    )

    service.add_reminder(reminder)

    result = service.mark_as_paid(3)

    assert result is True
    assert reminder.is_paid is True
    assert len(service.get_due_reminders()) == 0

    print("Mark as paid: PASS")


test_add_reminder()
test_due_reminders()
test_mark_as_paid()
