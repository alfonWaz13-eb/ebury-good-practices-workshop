class NotificationStrategy(ABC):

    @abstractmethod
    def send(self, deal):
        pass


class StandardNotification(NotificationStrategy):

    def send(self, deal):
        print(f"[Email] Deal {deal['id']} processed - Type: {deal['deal_type']}")


class PremiumNotification(NotificationStrategy):

    def send(self, deal):
        print(f"[Email] Deal {deal['id']} processed - Type: {deal['deal_type']}")
        print(f"[SMS] Premium client deal {deal['id']} confirmed")


class VIPNotification(NotificationStrategy):

    def send(self, deal):
        print(f"[Email] Deal {deal['id']} processed - Type: {deal['deal_type']}")
        print(f"[SMS] VIP client deal {deal['id']} confirmed")
        print(f"[Phone Call] Personal account manager will contact you about deal {deal['id']}")
