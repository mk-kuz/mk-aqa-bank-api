import random


class TestData:
    @staticmethod
    def valid_deposit_amount() -> float:
        return round(random.uniform(1000.0, 9000.0), 2)

    @staticmethod
    def invalid_deposit_amount() -> float:
        return round(random.uniform(1.0, 999.0), 2)

    @staticmethod
    def initial_sender_balance() -> float:
        return round(random.uniform(3000.0, 9000.0), 2)

    @staticmethod
    def initial_receiver_balance() -> float:
        return round(random.uniform(1000.0, 5000.0), 2)

    @staticmethod
    def valid_transfer_amount(max_amount: float = 2000.0) -> float:
        return round(random.uniform(500.0, max_amount), 2)

    @staticmethod
    def invalid_transfer_amount() -> float:
        return round(random.uniform(1.0, 499.0), 2)

    @staticmethod
    def valid_credit_amount() -> float:
        return round(random.uniform(5000.0, 9000.0), 2)

    @staticmethod
    def valid_credit_term() -> int:
        return random.choice([6, 12, 24])