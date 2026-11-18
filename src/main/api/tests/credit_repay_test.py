import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid_full_amount(self, api_manager, create_credit_user_request, db_session):
        account = api_manager.user_steps.create_account(create_credit_user_request)
        initial_balance = account.balance
        credit_amount = 5000.0
        term_months = 12

        credit = api_manager.user_steps.request_credit(
            create_credit_user_request,
            CreditRequest(accountId=account.id, amount=credit_amount, termMonths=term_months),
        )

        repay_request = CreditRepayRequest(creditId=credit.creditId, accountId=account.id, amount=credit_amount)
        response = api_manager.user_steps.repay_credit(create_credit_user_request, repay_request)
        credit_from_db = Credit.get_credit_by_id(db_session, credit.creditId)
        account_from_db = Account.get_account_by_id(db_session, account.id)

        assert response.creditId == credit.creditId
        assert response.amountDeposited == credit_amount
        assert credit_from_db.balance == 0.0
        assert account_from_db.balance == initial_balance

    def test_credit_repay_invalid_already_repaid(self, api_manager, create_credit_user_request, db_session):
        account = api_manager.user_steps.create_account(create_credit_user_request)
        initial_balance = account.balance
        credit_amount = 5000.0
        term_months = 12

        credit = api_manager.user_steps.request_credit(
            create_credit_user_request,
            CreditRequest(accountId=account.id, amount=credit_amount, termMonths=term_months),
        )

        repay_request = CreditRepayRequest(creditId=credit.creditId, accountId=account.id, amount=credit_amount)
        api_manager.user_steps.repay_credit(create_credit_user_request, repay_request)
        api_manager.user_steps.deposit(
            create_credit_user_request,
            DepositRequest(accountId=account.id, amount=credit_amount),
        )

        api_manager.user_steps.repay_credit_invalid(create_credit_user_request, repay_request)
        credit_from_db = Credit.get_credit_by_id(db_session, credit.creditId)
        account_from_db = Account.get_account_by_id(db_session, account.id)

        assert credit_from_db.balance == 0.0
        assert account_from_db.balance == initial_balance + credit_amount
