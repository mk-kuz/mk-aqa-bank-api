from typing import List
from sqlalchemy.orm import Session
from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:
    @staticmethod
    def get_transactions_by_to_account_id(db: Session, account_id: int) -> List[Transaction]:
        return db.query(Transaction).filter_by(to_account_id=account_id).all()

    @staticmethod
    def get_last_transaction_by_to_account_id(db: Session, account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(to_account_id=account_id).order_by(Transaction.id.desc()).first()

    @staticmethod
    def get_last_transaction_by_from_account_id(db: Session, account_id: int) -> Transaction | None:
        return db.query(Transaction).filter_by(from_account_id=account_id).order_by(Transaction.id.desc()).first()