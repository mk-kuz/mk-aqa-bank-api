import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.generators.test_data import TestData
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.utils.assert_helper import has_deposit_transaction


@pytest.mark.api
class TestDeposit:
    def test_deposit_valid_min_amount(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_account: CreateAccountResponse,
        db_session: Session,
    ):
        initial_balance = user_account.balance
        deposit_amount = TestData.valid_deposit_amount()

        deposit_request = DepositRequest(accountId=user_account.id, amount=deposit_amount)
        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        account_from_db = Account.get_account_by_id(db_session, user_account.id)
        transactions = Transaction.get_transactions_by_to_account_id(db_session, user_account.id)

        assert response.id == user_account.id, "Неверный счёт в ответе / депозит привязан к другому счёту"
        assert response.balance == round(initial_balance + deposit_amount, 2), "Неверный баланс в ответе / сумма депозита не учтена"
        assert account_from_db.balance == round(initial_balance + deposit_amount, 2), "Неверный баланс в БД / депозит не сохранился"
        assert has_deposit_transaction(transactions, deposit_amount), "Транзакция депозита не найдена / запись в истории не создана"

    def test_deposit_invalid_below_min_amount(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_account: CreateAccountResponse,
        db_session: Session,
    ):
        initial_balance = user_account.balance
        deposit_amount = TestData.invalid_deposit_amount()

        deposit_request = DepositRequest(accountId=user_account.id, amount=deposit_amount)
        api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)
        account_from_db = Account.get_account_by_id(db_session, user_account.id)

        assert account_from_db.balance == initial_balance, "Баланс изменился / отклонённый депозит не должен применяться"
