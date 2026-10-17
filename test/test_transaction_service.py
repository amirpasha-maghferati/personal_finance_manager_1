from service.transaction_service import TransactionService
from controller.transaction_controller import TransactionController


def test_add_transaction():
    service = TransactionService()

    controller = TransactionController()
    controller.create_transaction(
        1, 20000000, "income", "1", "حقوق"
    )

    assert len(controller.get_transactions()) == 1
    print("Add transaction: PASS")


def test_calculate_balance():
    controller = TransactionController()

    controller.create_transaction(
        1, 20000000, "income", "1", "حقوق"
    )

    controller.create_transaction(
        2, 2000000, "expense", "2", "خرید مایحتاج"
    )

    assert controller.get_balance() == 18000000
    print("Calculate balance: PASS")


def test_delete_transaction():
    controller = TransactionController()

    controller.create_transaction(
        1, 500000, "expense", "2", "خرید"
    )

    result = controller.delete_transaction(1)

    assert result is True
    assert len(controller.get_transactions()) == 0
    assert controller.get_balance() == 0

    print("Delete transaction: PASS")


def test_find_transaction():
    controller = TransactionController()

    controller.create_transaction(
        10, 1000000, "income", "1", "حقوق"
    )

    transaction = controller.service.find_transaction(10)

    assert transaction is not None
    assert transaction.amount == 1000000

    print("Find transaction: PASS")


test_add_transaction()
test_calculate_balance()
test_delete_transaction()
test_find_transaction()












from controller.transaction_controller import TransactionController


def test_update_transaction():
    controller = TransactionController()

    controller.create_transaction(
        1, 1000000, "income", "1", "حقوق"
    )

    result = controller.update_transaction(
        1, 1500000, "income", "1", "حقوق جدید"
    )

    transaction = controller.get_transactions()[0]

    assert result is True
    assert transaction.amount == 1500000
    assert transaction.description == "حقوق جدید"

    print("Update transaction: PASS")


test_update_transaction()




