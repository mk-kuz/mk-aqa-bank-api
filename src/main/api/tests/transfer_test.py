import pytest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.models.deposit_request import DepositRequest
from src.main.api.models.transfer_request import TransferRequest

@pytest.mark.api
class TestTransfer:
    def test_transfer_valid_between_own_accounts(self, api_manager, create_user_request, db_session):
        account_from = api_manager.user_steps.create_account(create_user_request)
        account_to = api_manager.user_steps.create_account(create_user_request)
        from_initial_balance = 3000.0
        to_initial_balance = 1000.0
        transfer_amount = 500.0

        api_manager.user_steps.deposit(
            create_user_request,
            DepositRequest(accountId=account_from.id, amount=from_initial_balance),
        )
        api_manager.user_steps.deposit(
            create_user_request,
            DepositRequest(accountId=account_to.id, amount=to_initial_balance),
        )

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

        assert response.fromAccountId == account_from.id
        assert response.toAccountId == account_to.id
        assert response.fromAccountIdBalance == from_initial_balance - transfer_amount
        assert account_from_db.balance == from_initial_balance - transfer_amount
        assert account_to_db.balance == to_initial_balance + transfer_amount
        assert sender_tx.amount == transfer_amount
        assert receiver_tx.amount == transfer_amount

    def test_transfer_invalid_below_min_amount(self, api_manager, create_user_request, db_session):
        account_from = api_manager.user_steps.create_account(create_user_request)
        account_to = api_manager.user_steps.create_account(create_user_request)
        from_initial_balance = 3000.0
        to_initial_balance = 1000.0

        api_manager.user_steps.deposit(
            create_user_request,
            DepositRequest(accountId=account_from.id, amount=from_initial_balance),
        )
        api_manager.user_steps.deposit(
            create_user_request,
            DepositRequest(accountId=account_to.id, amount=to_initial_balance),
        )

        transfer_request = TransferRequest(
            fromAccountId=account_from.id,
            toAccountId=account_to.id,
            amount=499.0,
        )
        api_manager.user_steps.transfer_invalid(create_user_request, transfer_request)

        account_from_db = Account.get_account_by_id(db_session, account_from.id)
        account_to_db = Account.get_account_by_id(db_session, account_to.id)

        assert account_from_db.balance == from_initial_balance
        assert account_to_db.balance == to_initial_balance