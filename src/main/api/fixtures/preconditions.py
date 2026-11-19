import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.generators.test_data import TestData
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.credit_response import CreditResponse
from src.main.api.models.deposit_request import DepositRequest


@pytest.fixture
def user_account(
    api_manager: ApiManager,
    create_user_request: CreateUserRequest,
) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(create_user_request)


@pytest.fixture
def credit_user_account(
    api_manager: ApiManager,
    create_credit_user_request: CreateUserRequest,
) -> CreateAccountResponse:
    return api_manager.user_steps.create_account(create_credit_user_request)


@pytest.fixture
def active_credit(
    api_manager: ApiManager,
    create_credit_user_request: CreateUserRequest,
    credit_user_account: CreateAccountResponse,
) -> CreditResponse:
    credit_request = CreditRequest(
        accountId=credit_user_account.id,
        amount=TestData.valid_credit_amount(),
        termMonths=TestData.valid_credit_term(),
    )
    return api_manager.user_steps.request_credit(create_credit_user_request, credit_request)


@pytest.fixture
def repaid_credit_with_balance(
    api_manager: ApiManager,
    create_credit_user_request: CreateUserRequest,
    credit_user_account: CreateAccountResponse,
    active_credit: CreditResponse,
) -> CreditResponse:
    repay_request = CreditRepayRequest(
        creditId=active_credit.creditId,
        accountId=credit_user_account.id,
        amount=active_credit.amount,
    )
    api_manager.user_steps.repay_credit(create_credit_user_request, repay_request)
    api_manager.user_steps.deposit(
        create_credit_user_request,
        DepositRequest(accountId=credit_user_account.id, amount=active_credit.amount),
    )
    return active_credit


@pytest.fixture
def funded_transfer_accounts(
    api_manager: ApiManager,
    create_user_request: CreateUserRequest,
) -> tuple[CreateAccountResponse, float, CreateAccountResponse, float]:
    account_from = api_manager.user_steps.create_account(create_user_request)
    account_to = api_manager.user_steps.create_account(create_user_request)

    from_initial_balance = TestData.initial_sender_balance()
    to_initial_balance = TestData.initial_receiver_balance()

    api_manager.user_steps.deposit(
        create_user_request,
        DepositRequest(accountId=account_from.id, amount=from_initial_balance),
    )
    api_manager.user_steps.deposit(
        create_user_request,
        DepositRequest(accountId=account_to.id, amount=to_initial_balance),
    )
    return account_from, from_initial_balance, account_to, to_initial_balance
