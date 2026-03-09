from abc import ABC, abstractmethod


class NotificationService(ABC):

    @abstractmethod
    def send_funds_assignation_notification(self, recipient):
        pass


class EmailNotificationService(NotificationService):

    def send_funds_assignation_notification(self, recipient):
        print(f"[Email] Sending email to {recipient}")
        return True
