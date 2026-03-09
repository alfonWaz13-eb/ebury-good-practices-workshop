class DealTypeStrategy(ABC):

    @abstractmethod
    def process(self, deal, deal_data):
        pass

    @abstractmethod
    def calculate_risk(self, deal):
        pass

    def get_base_rate(self, currency_pair):
        base_rates = {
            'EUR/USD': 1.08,
            'GBP/EUR': 1.17,
            'USD/GBP': 0.79
        }
        return base_rates.get(currency_pair, 1.0)


class SpotDealStrategy(DealTypeStrategy):

    rates = {
        'EUR/USD': 1.08,
        'GBP/EUR': 1.17,
        'USD/GBP': 0.79
    }

    def process(self, deal, deal_data):
        deal['rate'] = self.get_base_rate(deal['currency_pair'])
        deal['maturity_days'] = 2

    def calculate_risk(self, deal):
        risk_score = deal['amount'] * 0.01
        exposure = deal['amount']
        return {
            'risk_score': risk_score,
            'exposure': exposure,
            'risk_level': 'high' if risk_score > 1000 else 'low'
        }


class DrawdownDealStrategy(DealTypeStrategy):

    def process(self, deal, deal_data):
        days = deal_data.get('drawdown_days', 30)
        deal['rate'] = self._get_drawdown_rate(deal['currency_pair'], days)
        deal['maturity_days'] = days

    def calculate_risk(self, deal):
        risk_score = deal['amount'] * 0.03
        exposure = deal['amount'] * 1.5
        return {
            'risk_score': risk_score,
            'exposure': exposure,
            'risk_level': 'high' if risk_score > 1000 else 'low'
        }

    def _get_drawdown_rate(self, currency_pair, days):
        base_rate = self.get_base_rate(currency_pair)
        drawdown_points = days * 0.0001
        return base_rate + drawdown_points


class SettlementDealStrategy(DealTypeStrategy):

    spot_strategy = SpotDealStrategy()

    def process(self, deal, deal_data):
        deal['near_leg_rate'] = self._get_settlement_rate(deal['currency_pair'])
        deal['maturity_days'] = deal_data.get('settlement_days', 90)

    def calculate_risk(self, deal):
        risk_score = deal['amount'] * 0.05
        exposure = deal['amount'] * 2.0
        return {
            'risk_score': risk_score,
            'exposure': exposure,
            'risk_level': 'high' if risk_score > 1000 else 'low'
        }

    def _get_settlement_rate(self, currency_pair):
        base_rate = self.get_base_rate(currency_pair)
        settlement_points = 0.0005
        return base_rate + settlement_points
