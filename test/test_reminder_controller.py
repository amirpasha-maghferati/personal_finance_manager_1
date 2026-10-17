from datetime import date, timedelta

from controller.reminder_controller import ReminderController


def test_create_reminder():
    controller = ReminderController()

    controller.create_reminder(
        1,
        "پرداخت اجاره",
        5000000,
        date.today() + timedelta(days=30),
        "2"
    )

    assert len(controller.get_reminders()) == 1
    print("Create reminder: PASS")


def test_get_due_reminders():
    controller = ReminderController()

    controller.create_reminder(
        2,
        "پرداخت قبض",
        200000,
        date.today() - timedelta(days=1),
        "2"
    )

    due_reminders = controller.get_due_reminders()

    assert len(due_reminders) == 1
    print("Get due reminders: PASS")


def test_mark_as_paid():
    controller = ReminderController()

    controller.create_reminder(
        3,
        "پرداخت قسط",
        1000000,
        date.today(),
        "2"
    )

    result = controller.mark_as_paid(3)

    assert result is True
    assert len(controller.get_due_reminders()) == 0

    print("Mark as paid: PASS")


test_create_reminder()
test_get_due_reminders()
test_mark_as_paid()











def test_delete_reminder():
    controller = ReminderController()

    controller.create_reminder(
        10,
        "پرداخت قبض",
        200000,
        date.today() + timedelta(days=10),
        "2"
    )

    result = controller.delete_reminder(10)

    assert result is True
    assert len(controller.get_reminders()) == 0

    print("Delete reminder: PASS")


test_delete_reminder()

