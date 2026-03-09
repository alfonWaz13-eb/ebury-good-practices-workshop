from abc import ABC, abstractmethod
from datetime import datetime

from open_close.with_principle.deal_type import SpotDealStrategy, DrawdownDealStrategy, SettlementDealStrategy
from open_close.with_principle.fee_calculator import StandardFeeCalculatorStrategy, PremiumFeeCalculatorStrategy, VIPFeeCalculatorStrategy
from open_close.with_principle.notification import StandardNotification, PremiumNotification, VIPNotification


class FXDealProcessor:

    def __init__(self):
        self.deals = []
        self._deal_strategies = {
            'spot': SpotDealStrategy(),
            'drawdown': DrawdownDealStrategy(),
            'settlement': SettlementDealStrategy()
        }
        self._fee_calculators = {
            'standard': StandardFeeCalculatorStrategy(),
            'premium': PremiumFeeCalculatorStrategy(),
            'vip': VIPFeeCalculatorStrategy()
        }
        self._notification_strategies = {
            'standard': StandardNotification(),
            'premium': PremiumNotification(),
            'vip': VIPNotification()
        }

    def process_deal(self, deal_data):
        deal_type = deal_data.get('deal_type', 'spot')
        client_type = deal_data.get('client_type', 'standard')

        deal = {
            'id': len(self.deals) + 1,
            'currency_pair': deal_data['currency_pair'],
            'amount': deal_data['amount'],
            'deal_type': deal_type,
            'client_type': client_type,
            'timestamp': datetime.now().isoformat()
        }

        deal_strategy = self._deal_strategies.get(deal_type)
        if not deal_strategy:
            raise ValueError(f"Unknown deal type: {deal_type}")

        deal_strategy.process(deal, deal_data)

        fee_calculator = self._fee_calculators.get(client_type, StandardFeeCalculatorStrategy())
        fee = fee_calculator.calculate_fee(deal['amount'])
        deal['fee'] = fee
        deal['net_amount'] = deal['amount'] - fee

        notification_strategy = self._notification_strategies.get(client_type)
        if notification_strategy:
            notification_strategy.send(deal)

        self.deals.append(deal)
        return deal

    def calculate_risk_metrics(self, deal):
        deal_type = deal['deal_type']
        deal_strategy = self._deal_strategies.get(deal_type)

        if not deal_strategy:
            return {
                'risk_score': 0,
                'exposure': 0,
                'risk_level': 'low'
            }

        return deal_strategy.calculate_risk(deal)

    def apply_discount(self, deal_data):
        client_type = deal_data.get('client_type', 'standard')
        amount = deal_data['amount']
        
        fee_calculator = self._fee_calculators.get(client_type, StandardFeeCalculatorStrategy())
        return fee_calculator.apply_discount(amount)


if __name__ == "__main__":
    processor = FXDealProcessor()
    
    spot_deal = processor.process_deal({
        'currency_pair': 'EUR/USD',
        'amount': 50000,
        'deal_type': 'spot',
        'client_type': 'standard'
    })
    print(f"Spot deal processed: {spot_deal}")
    
    drawdown_deal = processor.process_deal({
        'currency_pair': 'GBP/EUR',
        'amount': 100000,
        'deal_type': 'drawdown',
        'drawdown_days': 60,
        'client_type': 'premium'
    })
    print(f"Forward deal processed: {drawdown_deal}")
    
    risk = processor.calculate_risk_metrics(spot_deal)
    print(f"Risk metrics: {risk}")

