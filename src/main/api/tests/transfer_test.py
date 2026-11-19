import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.generators.test_data import TestData
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_request import TransferRequest


@pytest.mark.api
class TestTransfer:
    def test_transfer_valid_between_own_accounts(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        funded_transfer_accounts: tuple[CreateAccountResponse, float, CreateAccountResponse, float],
        db_session: Session,
    ):
        account_from, from_initial_balance, account_to, to_initial_balance = funded_transfer_accounts
        transfer_amount = TestData.valid_transfer_amount(max_amount=from_initial_balance)

        transfer_request = TransferRequest(
            fromAccountId=account_from.id,
            toAccountId=account_to.id,
            amount=transfer_amount,
        )
        response = api_manager.user_steps.transfer(create_user_request, transfer_request)

        account_from_db = Account.get_account_by_id(db_session, account_from.id)
        account_to_db = Account.get_account_by_id(db_session, account_to.id)
        sender_tx = Transaction.get_last_transaction_by_from_account_id(db_session, account_from.id)
        receiver_tx = Transaction.get_last_transaction_by_to_account_id(db_session, account_to.id)

        assert response.fromAccountId == account_from.id, "Неверный счёт отправителя в ответе / указан другой источник"
        assert response.toAccountId == account_to.id, "Неверный счёт получателя в ответе / указан другой получатель"
        assert round(response.fromAccountIdBalance, 2) == round(from_initial_balance - transfer_amount, 2), "Неверный баланс отправителя в ответе / списание рассчитано некорректно"
        assert account_from_db.balance == round(from_initial_balance - transfer_amount, 2), "Неверный баланс отправителя в БД / списание не сохранено"
        assert account_to_db.balance == round(to_initial_balance + transfer_amount, 2), "Неверный баланс получателя в БД / зачисление не сохранено"
        assert sender_tx.amount == transfer_amount, "Неверная сумма транзакции отправителя / списание записано некорректно"
        assert receiver_tx.amount == transfer_amount, "Неверная сумма транзакции получателя / зачисление записано некорректно"

    def test_transfer_invalid_below_min_amount(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        funded_transfer_accounts: tuple[CreateAccountResponse, float, CreateAccountResponse, float],
        db_session: Session,
    ):
        account_from, from_initial_balance, account_to, to_initial_balance = funded_transfer_accounts
        transfer_amount = TestData.invalid_transfer_amount()

        transfer_request = TransferRequest(
            fromAccountId=account_from.id,
            toAccountId=account_to.id,
            amount=transfer_amount,
        )
        api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        account_from_db = Account.get_account_by_id(db_session, account_from.id)
        account_to_db = Account.get_account_by_id(db_session, account_to.id)

        assert account_from_db.balance == from_initial_balance, "Баланс отправителя изменился / отклонённый перевод не должен списывать средства"
        assert account_to_db.balance == to_initial_balance, "Баланс получателя изменился / отклонённый перевод не должен зачислять средства"