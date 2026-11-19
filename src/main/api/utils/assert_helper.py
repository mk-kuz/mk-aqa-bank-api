from typing import Any


def has_deposit_transaction(transactions: list[Any], amount: float) -> bool:
    return any(
        t.transaction_type == "deposit" and t.amount == amount
        for t in transactions
    )