import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestDeposit:
    def test_deposit_valid_min_amount(self, api_manager, create_user_request, db_session):
        account = api_manager.user_steps.create_account(create_user_request)
        initial_balance = account.balance
        deposit_amount = 1000.0

        deposit_request = DepositRequest(accountId=account.id, amount=deposit_amount)
        response = api_manager.user_steps.deposit(create_user_request, deposit_request)

        account_from_db = Account.get_account_by_id(db_session, account.id)
        transactions = Transaction.get_transactions_by_to_account_id(db_session, account.id)

        assert response.id == account.id
        assert response.balance == initial_balance + deposit_amount
        assert account_from_db.balance == initial_balance + deposit_amount
        assert any(t.transaction_type == "deposit" and t.amount == deposit_amount for t in transactions)

    def test_deposit_invalid_below_min_amount(self, api_manager, create_user_request, db_session):
        account = api_manager.user_steps.create_account(create_user_request)
        initial_balance = account.balance

        deposit_request = DepositRequest(accountId=account.id, amount=999.0)
        api_manager.user_steps.deposit_invalid(create_user_request, deposit_request)
        account_from_db = Account.get_account_by_id(db_session, account.id)

        assert account_from_db.balance == initial_balance
