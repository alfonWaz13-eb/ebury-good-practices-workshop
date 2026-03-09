from abc import ABC, abstractmethod


class DatabaseRepository(ABC):

    @abstractmethod
    def save_assignation(self, assignation_data):
        pass

    @abstractmethod
    def get_account_balance(self, account_id):
        pass


class MySQLDatabase(DatabaseRepository):

    def save_assignation(self, assignation_data):
        print(f"[MySQL] Saving assignation")
        print(f"[MySQL] Data: {assignation_data}")
        return True

    def get_account_balance(self, account_id):
        balances = {
            'ACC001': 100000.0,
            'ACC002': 50000.0,
            'ACC003': 250000.0
        }
        return balances.get(account_id, 0.0)
