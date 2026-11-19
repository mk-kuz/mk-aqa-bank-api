import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_response import CreditResponse


@pytest.mark.api
class TestCreditRepay:
    def test_credit_repay_valid_full_amount(
        self,
        api_manager: ApiManager,
        create_credit_user_request: CreateUserRequest,
        credit_user_account: CreateAccountResponse,
        active_credit: CreditResponse,
        db_session: Session,
    ):
        repay_request = CreditRepayRequest(
            creditId=active_credit.creditId,
            accountId=credit_user_account.id,
            amount=active_credit.amount,
        )
        response = api_manager.user_steps.repay_credit(create_credit_user_request, repay_request)

        credit_from_db = Credit.get_credit_by_id(db_session, active_credit.creditId)
        account_from_db = Account.get_account_by_id(db_session, credit_user_account.id)

        assert response.creditId == active_credit.creditId, "Неверный идентификатор кредита в ответе / погашён другой кредит"
        assert response.amountDeposited == active_credit.amount, "Неверная сумма погашения в ответе / возвращено некорректное значение"
        assert credit_from_db.balance == 0.0, "Остаток по кредиту не обнулён / кредит не погашен полностью"
        assert account_from_db.balance == credit_user_account.balance, "Неверный баланс счёта после погашения / средства списаны некорректно"

    def test_credit_repay_invalid_already_repaid(
        self,
        api_manager: ApiManager,
        create_credit_user_request: CreateUserRequest,
        credit_user_account: CreateAccountResponse,
        repaid_credit_with_balance: CreditResponse,
        db_session: Session,
    ):
        repay_request = CreditRepayRequest(
            creditId=repaid_credit_with_balance.creditId,
            accountId=credit_user_account.id,
            amount=repaid_credit_with_balance.amount,
        )
        api_manager.user_steps.repay_credit_invalid(create_credit_user_request, repay_request)

        credit_from_db = Credit.get_credit_by_id(db_session, repaid_credit_with_balance.creditId)
        account_from_db = Account.get_account_by_id(db_session, credit_user_account.id)

        assert credit_from_db.balance == 0.0, "Остаток по кредиту изменился / повторное погашение не должно применяться"
        assert account_from_db.balance == credit_user_account.balance + repaid_credit_with_balance.amount, "Баланс счёта изменился / повторное списание не должно выполняться"
