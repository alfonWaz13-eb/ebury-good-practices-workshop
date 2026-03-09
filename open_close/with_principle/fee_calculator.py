class FeeCalculatorStrategy(ABC):

    @abstractmethod
    def calculate_fee(self, amount):
        pass

    @abstractmethod
    def apply_discount(self, amount):
        pass


class StandardFeeCalculatorStrategy(FeeCalculatorStrategy):

    def calculate_fee(self, amount):
        return amount * 0.001

    def apply_discount(self, amount):
        return amount


class PremiumFeeCalculatorStrategy(FeeCalculatorStrategy):

    def calculate_fee(self, amount):
        return amount * 0.0005

    def apply_discount(self, amount):
        if amount > 100000:
            return amount * 0.99
        return amount


class VIPFeeCalculatorStrategy(FeeCalculatorStrategy):

    def calculate_fee(self, amount):
        return 0

    def apply_discount(self, amount):
        if amount > 100000:
            return amount * 0.98
        elif amount > 50000:
            return amount * 0.99
        return amount
