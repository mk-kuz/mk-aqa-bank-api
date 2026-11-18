import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_request import CreditRequest


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid_for_credit_role(self, api_manager, create_credit_user_request, db_session):
        account = api_manager.user_steps.create_account(create_credit_user_request)
        initial_balance = account.balance
        credit_amount = 5000.0
        term_months = 12

        credit_request = CreditRequest(accountId=account.id, amount=credit_amount, termMonths=term_months)
        response = api_manager.user_steps.request_credit(create_credit_user_request, credit_request)
        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        account_from_db = Account.get_account_by_id(db_session, account.id)

        assert response.amount == credit_amount
        assert response.balance == credit_amount
        assert credit_from_db is not None
        assert credit_from_db.account_id == account.id
        assert credit_from_db.amount == credit_amount
        assert credit_from_db.term_months == term_months
        assert credit_from_db.balance == -credit_amount
        assert account_from_db.balance == initial_balance + credit_amount

    def test_credit_request_invalid_for_regular_user_role(self, api_manager, create_user_request, db_session):
        account = api_manager.user_steps.create_account(create_user_request)
        initial_balance = account.balance
        credit_amount = 5000.0
        term_months = 12

        credit_request = CreditRequest(accountId=account.id, amount=credit_amount, termMonths=term_months)
        api_manager.user_steps.request_credit_forbidden(create_user_request, credit_request)
        account_from_db = Account.get_account_by_id(db_session, account.id)
        credits_from_db = Credit.get_credits_by_account_id(db_session, account.id)

        assert account_from_db.balance == initial_balance
        assert len(credits_from_db) == 0
