from datetime import datetime


class FXDealProcessor:

    def __init__(self):
        self.deals = []

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

        if deal_type == 'spot':
            deal['rate'] = self._get_spot_rate(deal['currency_pair'])
            deal['maturity_days'] = 2
        elif deal_type == 'drawdown':
            deal['rate'] = self._get_drawdown_rate(deal['currency_pair'], deal_data.get('drawdown_days', 30))
            deal['maturity_days'] = deal_data.get('drawdown_days', 30)
        elif deal_type == 'settlement':
            deal['near_leg_rate'] = self._get_settlement_rate(deal['currency_pair'])
            deal['maturity_days'] = deal_data.get('settlement_days', 90)
        else:
            raise ValueError(f"Unknown deal type: {deal_type}")

        if client_type == 'standard':
            fee = deal['amount'] * 0.001
        elif client_type == 'premium':
            fee = deal['amount'] * 0.0005
        elif client_type == 'vip':
            fee = 0
        else:
            fee = deal['amount'] * 0.002

        deal['fee'] = fee
        deal['net_amount'] = deal['amount'] - fee

        if client_type == 'standard':
            self._send_standard_notification(deal)
        elif client_type == 'premium':
            self._send_premium_notification(deal)
        elif client_type == 'vip':
            self._send_vip_notification(deal)

        self.deals.append(deal)
        return deal

    def _get_spot_rate(self, currency_pair):
        rates = {
            'EUR/USD': 1.08,
            'GBP/EUR': 1.17,
            'USD/GBP': 0.79
        }
        return rates.get(currency_pair, 1.0)

    def _get_drawdown_rate(self, currency_pair, days):
        spot_rate = self._get_spot_rate(currency_pair)
        drawdown_points = days * 0.0001
        return spot_rate + drawdown_points

    def _get_settlement_rate(self, currency_pair):
        spot_rate = self._get_spot_rate(currency_pair)
        settlement_points = 0.0005
        return spot_rate + settlement_points

    def _send_standard_notification(self, deal):
        print(f"[Email] Deal {deal['id']} processed - Type: {deal['deal_type']}")

    def _send_premium_notification(self, deal):
        print(f"[Email] Deal {deal['id']} processed - Type: {deal['deal_type']}")
        print(f"[SMS] Premium client deal {deal['id']} confirmed")

    def _send_vip_notification(self, deal):
        print(f"[Email] Deal {deal['id']} processed - Type: {deal['deal_type']}")
        print(f"[SMS] VIP client deal {deal['id']} confirmed")
        print(f"[Phone Call] Personal account manager will contact you about deal {deal['id']}")

    def calculate_risk_metrics(self, deal):
        deal_type = deal['deal_type']
        
        if deal_type == 'spot':
            risk_score = deal['amount'] * 0.01
            exposure = deal['amount']
        elif deal_type == 'drawdown':
            risk_score = deal['amount'] * 0.03
            exposure = deal['amount'] * 1.5
        elif deal_type == 'settlement':
            risk_score = deal['amount'] * 0.05
            exposure = deal['amount'] * 2.0
        else:
            risk_score = 0
            exposure = 0

        return {
            'risk_score': risk_score,
            'exposure': exposure,
            'risk_level': 'high' if risk_score > 1000 else 'low'
        }

    def apply_discount(self, deal_data):
        client_type = deal_data.get('client_type', 'standard')
        amount = deal_data['amount']
        
        if client_type == 'standard':
            return amount
        elif client_type == 'premium':
            if amount > 100000:
                return amount * 0.99
            return amount
        elif client_type == 'vip':
            if amount > 100000:
                return amount * 0.98
            elif amount > 50000:
                return amount * 0.99
            return amount
        else:
            return amount


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

