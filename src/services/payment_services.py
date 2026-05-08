from src.models.exceptions import ValidationError
from src.models.payment import Payment, PaymentMethod
from abc import ABC, abstractmethod


class PaymentValidate:
    @staticmethod
    def validate_payment(payment: Payment):
        """Валидация платежа"""
        if not isinstance(payment.order_id, (int)):
            raise ValidationError("id должен быть числом")
        if payment.order_id <= 0:
            raise ValidationError("id должен быть положительным числом")
        if not isinstance(payment.amount, (int, float)):
            raise ValidationError("Сумма должна быть числом")
        if payment.amount <= 0:
            raise ValidationError("Сумма должна быть положительной")
        return True
        


class NotificationService(ABC):
    """Абстрактный класс для реализации отправки уведомлений"""
    @abstractmethod
    def send_notification(self):
        pass


class EmailNotifical(NotificationService):
    """Класс для отправки уведомлений по email"""

    def send_notification(self, payment: Payment):
        """Отправка уведомления"""
        print(f"Отправка email о платеже заказа с id: {payment.order_id}")
             

class SmsNotitfical(NotificationService):  # Можно добавлять другие способы отправки уведомлений
    pass


class TelegramNotifical(NotificationService):
    pass
        

class Database(ABC):
    """Абстрактный класс реализаций сохранения информации о платеже в различные БД"""

    @abstractmethod
    def save_to_database(self):
        pass


class SavePsQL(Database):
    
    def save_to_database(self, payment: Payment):
        """Сохранение в БД"""
        print(f"Сохранение платежа с id: {payment.order_id} в PsQL")

class SaveMySQL(Database):  # Можно добавить реализацию другой БД
    pass
    
    
class PaymentProcessor:

    def __init__(self, payment_method: PaymentMethod, repository: Database, notification_service: NotificationService):
        self.payment_method = payment_method
        self.repository = repository
        self.notification_service = notification_service

    def process_payment(self, payment: Payment):

        PaymentValidate.validate_payment(payment)

        res = self.payment_method.process(payment.amount)

        if res:
            payment.status = "completed"
        else:
            payment.status = "failed"
            raise ValueError(f"Ошибка обработки платежа методом {type(self.payment_method).__name__}")
        
        self.repository.save_to_database(payment)

        self.notification_service.send_notification(payment)

        return payment.status
    
