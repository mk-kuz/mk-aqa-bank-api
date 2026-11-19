from sqlalchemy.orm import Session
from src.main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        return db.query(User).filter_by(username=username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        return db.query(User).filter_by(id=user_id).first()