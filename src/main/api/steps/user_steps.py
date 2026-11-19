from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request import CreditRequest
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.CREATE_ACCOUNT,
            ResponseSpecs.request_created(),
        ).post()

    def deposit(self, user_request: CreateUserRequest, deposit_request: DepositRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_ok(),
        ).post(deposit_request)

    def deposit_invalid(self, user_request: CreateUserRequest, deposit_request: DepositRequest):
        return CrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(deposit_request)

    def transfer(self, user_request: CreateUserRequest, transfer_request: TransferRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_ok(),
        ).post(transfer_request)

    def transfer_invalid(self, user_request: CreateUserRequest, transfer_request: TransferRequest):
        return CrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.request_bad(),
        ).post(transfer_request)

    def get_account_transactions(self, user_request: CreateUserRequest, account_id: int):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.GET_ACCOUNT_TRANSACTIONS,
            ResponseSpecs.request_ok(),
        ).get(account_id)

    def request_credit(self, user_request: CreateUserRequest, credit_request: CreditRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_created(),
        ).post(credit_request)

    def request_credit_forbidden(self, user_request: CreateUserRequest, credit_request: CreditRequest):
        return CrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.REQUEST_CREDIT,
            ResponseSpecs.request_forbidden(),
        ).post(credit_request)

    def repay_credit(self, user_request: CreateUserRequest, repay_request: CreditRepayRequest):
        return ValidateCrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_ok(),
        ).post(repay_request)

    def repay_credit_invalid(self, user_request: CreateUserRequest, repay_request: CreditRepayRequest):
        return CrudRequester(
            RequestSpecs.auth_headers(username=user_request.username, password=user_request.password),
            Endpoint.REPAY_CREDIT,
            ResponseSpecs.request_conflict(),
        ).post(repay_request)
