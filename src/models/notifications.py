from abc import ABC, abstractmethod


class Notification(ABC):
    """Абстрактный класс для уведомлений"""
    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotification(Notification):
    """Отправка уведомлений по email"""
    def __init__(self, email: str):
        self.email = email

    def send(self, message: str):
        print(f"Уведомление отправлено на email {self.email}: {message}")


class SmsNotification(Notification):
    """Отправка уведомления по смс"""
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def send(self, message: str):
        print(f"Уведомление отправлено по смс на номер {self.phone_number}: {message}")


def process_notifications(notifications: list[Notification], message: str):
    """Обработка уведомления"""
    for notification in notifications:
        notification.send(message)

# экземпляры классов куда отправлять уведомления
email_notification = EmailNotification("spk60150@gmail.com")
sms_notification = SmsNotification("+7 925 965 58 20")


notifications = [email_notification, sms_notification]
process_notifications(notifications, "Ваш заказ готов")