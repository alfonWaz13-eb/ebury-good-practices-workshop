from datetime import datetime


class FXDealProcessor:

    def __init__(self):
        self.deals = []
        self.db_connection = 'db_connection_string'
        self.exchange_rates = {
            'EUR/USD': 1.08,
            'GBP/EUR': 1.17,
            'USD/GBP': 0.79
        }

    def add_deal(self, deal_data):
        deal = {
            'id': len(self.deals) + 1,
            'currency_pair': deal_data['currency_pair'],
            'amount': deal_data['amount'],
            'rate': deal_data.get('rate'),
            'client_email': deal_data['client_email'],
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }

        if not self._validate_deal(deal):
            raise ValueError("Deal validation failed")

        if not deal['rate']:
            deal['rate'] = self._get_exchange_rate(deal['currency_pair'])

        deal['converted_amount'] = deal['amount'] * deal['rate']

        self.deals.append(deal)
        self._save_to_database(deal)
        self._send_confirmation_email(deal)
        self._log_transaction(deal, 'CREATE')

        return deal

    def _validate_deal(self, deal):
        if deal['amount'] <= 0:
            return False
        if deal['amount'] > 1000000:
            return False
        if deal['currency_pair'] not in self.exchange_rates:
            return False
        return True

    def _get_exchange_rate(self, currency_pair):
        return self.exchange_rates.get(currency_pair, 1.0)

    def _save_to_database(self, deal):
        print(f"Saving {deal['id']} to database: {self.db_connection}")

    def _send_confirmation_email(self, deal):
        print(f"Sending email to: {deal['client_email']}")
        print(f"""Your FX deal has been confirmed:
        - Currency Pair: {deal['currency_pair']}
        - Amount: {deal['amount']}
        - Rate: {deal['rate']}
        - Converted Amount: {deal['converted_amount']}
        """)

    def _log_transaction(self, deal, action):
        log_entry = f"[{datetime.now()}] {action} - Deal ID: {deal['id']} - {deal['currency_pair']}"
        print(f"Audit log: {log_entry}")

    def generate_daily_report(self):
        total_volume = sum(deal['converted_amount'] for deal in self.deals)
        report = {
            'date': datetime.now().isoformat(),
            'total_deals': len(self.deals),
            'total_volume_usd': total_volume,
            'deals': self.deals
        }
        print(report)

        self._send_report_email(report)

        return report

    def _send_report_email(self, report_content):
        print(f"Sending report to managers@company.com")
        print(f"   Report content: {report_content}...")


if __name__ == "__main__":

    processor = FXDealProcessor()
    deal_data = {
        'currency_pair': 'EUR/USD',
        'amount': 50000,
        'client_email': 'client@example.com'
    }
    deal = processor.add_deal(deal_data)
    processor.generate_daily_report()

