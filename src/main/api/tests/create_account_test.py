import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.user_steps.create_account(create_user_request)
        assert response.balance == 0, "Неверный начальный баланс / счёт создан не с нулевым балансом"

        acc_from_db = Account.get_account_by_id(db_session, response.id)
        assert acc_from_db.id == response.id, "Счёт не найден в БД / id в базе не совпадает с ответом"
        assert acc_from_db.balance is not None, "Баланс счёта в БД отсутствует / значение не сохранено"