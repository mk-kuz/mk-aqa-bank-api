import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit
from src.main.api.generators.test_data import TestData
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request import CreditRequest


@pytest.mark.api
class TestCreditRequest:
    def test_credit_request_valid_for_credit_role(
        self,
        api_manager: ApiManager,
        create_credit_user_request: CreateUserRequest,
        credit_user_account: CreateAccountResponse,
        db_session: Session,
    ):
        initial_balance = credit_user_account.balance
        credit_amount = TestData.valid_credit_amount()
        term_months = TestData.valid_credit_term()

        credit_request = CreditRequest(accountId=credit_user_account.id, amount=credit_amount, termMonths=term_months)
        response = api_manager.user_steps.request_credit(create_credit_user_request, credit_request)
        credit_from_db = Credit.get_credit_by_id(db_session, response.creditId)
        account_from_db = Account.get_account_by_id(db_session, credit_user_account.id)

        assert response.amount == credit_amount, "Неверная сумма кредита в ответе / возвращено некорректное значение"
        assert response.balance == credit_amount, "Неверный баланс кредита в ответе / остаток по кредиту рассчитан неверно"
        assert credit_from_db is not None, "Кредит не найден в БД / запись не создана после одобрения"
        assert credit_from_db.account_id == credit_user_account.id, "Кредит привязан к другому счёту / неверный account_id в БД"
        assert credit_from_db.amount == credit_amount, "Неверная сумма кредита в БД / сохранено некорректное значение"
        assert credit_from_db.term_months == term_months, "Неверный срок кредита в БД / сохранено некорректное значение"
        assert credit_from_db.balance == -credit_amount, "Неверный остаток по кредиту в БД / долг рассчитан некорректно"
        assert account_from_db.balance == initial_balance + credit_amount, "Неверный баланс счёта / сумма кредита не зачислена"

    def test_credit_request_invalid_for_regular_user_role(
        self,
        api_manager: ApiManager,
        create_user_request: CreateUserRequest,
        user_account: CreateAccountResponse,
        db_session: Session,
    ):
        initial_balance = user_account.balance
        credit_amount = TestData.valid_credit_amount()
        term_months = TestData.valid_credit_term()

        credit_request = CreditRequest(accountId=user_account.id, amount=credit_amount, termMonths=term_months)
        api_manager.user_steps.request_credit_forbidden(create_user_request, credit_request)
        account_from_db = Account.get_account_by_id(db_session, user_account.id)
        credits_from_db = Credit.get_credits_by_account_id(db_session, user_account.id)

        assert account_from_db.balance == initial_balance, "Баланс счёта изменился / кредит не должен быть выдан"
        assert len(credits_from_db) == 0, "В БД созданы записи кредита / кредит не должен быть оформлен"
