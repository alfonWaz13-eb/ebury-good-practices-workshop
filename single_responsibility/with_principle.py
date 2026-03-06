from datetime import datetime


class DealValidator:

    def validate(self, deal):
        if deal['amount'] <= 0:
            return False
        if deal['amount'] > 1000000:
            return False
        return True


class ExchangeRateService:

    def __init__(self):
        self.exchange_rates = {
            'EUR/USD': 1.08,
            'GBP/EUR': 1.17,
            'USD/GBP': 0.79
        }

    def get_rate(self, currency_pair):
        return self.exchange_rates.get(currency_pair, 1.0)


class DealRepository:

    def __init__(self, db_connection):
        self.deals = []
        self.db_connection = db_connection

    def save(self, deal):
        self.deals.append(deal)
        print(f"Saving {deal['id']} to database: {self.db_connection}")

    def get_all(self):
        return self.deals


class EmailNotificationService:

    def send_confirmation(self, deal):
        print(f"Sending email to: {deal['client_email']}")
        print(f"""Your FX deal has been confirmed:
        - Currency Pair: {deal['currency_pair']}
        - Amount: {deal['amount']}
        - Rate: {deal['rate']}
        - Converted Amount: {deal['converted_amount']}
        """)

    def send_report(self, report_content):
        print(f"Sending report to managers@company.com")
        print(f"   Report content: {report_content}...")


class AuditLogger:

    def log(self, deal, action):
        log_entry = f"[{datetime.now()}] {action} - Deal ID: {deal['id']} - {deal['currency_pair']}"
        print(f"Audit log: {log_entry}")


class ReportGenerator:

    def generate_daily_report(self, deals):
        total_volume = sum(deal['converted_amount'] for deal in deals)
        report = {
            'date': datetime.now().isoformat(),
            'total_deals': len(deals),
            'total_volume_usd': total_volume,
            'deals': deals
        }
        print(report)
        return report


class FXDealProcessor:

    def __init__(
            self,
            exchange_rate_service=ExchangeRateService(),
            validator=DealValidator(),
            repository=DealRepository(db_connection='db_connection_string'),
            email_service=EmailNotificationService(),
            audit_logger=AuditLogger(),
            report_generator=ReportGenerator()
    ):
        self.exchange_rate_service = exchange_rate_service
        self.validator = validator
        self.repository = repository
        self.email_service = email_service
        self.audit_logger = audit_logger
        self.report_generator = report_generator

    def add_deal(self, deal_data):
        deal = {
            'id': len(self.repository.get_all()) + 1,
            'currency_pair': deal_data['currency_pair'],
            'amount': deal_data['amount'],
            'rate': deal_data.get('rate'),
            'client_email': deal_data['client_email'],
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }

        if not self.validator.validate(deal):
            raise ValueError("Deal validation failed")

        if not deal['rate']:
            deal['rate'] = self.exchange_rate_service.get_rate(deal['currency_pair'])

        deal['converted_amount'] = deal['amount'] * deal['rate']

        self.repository.save(deal)
        self.email_service.send_confirmation(deal)
        self.audit_logger.log(deal, 'CREATE')

        return deal

    def generate_daily_report(self):
        report = self.report_generator.generate_daily_report(deals=self.repository.get_all())
        self.email_service.send_report(report)
        return report


if __name__ == "__main__":

    processor = FXDealProcessor()
    deal_data = {
        'currency_pair': 'EUR/USD',
        'amount': 50000,
        'client_email': 'client@example.com'
    }
    deal = processor.add_deal(deal_data)
    processor.generate_daily_report()

