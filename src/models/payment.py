from abc import ABC, abstractmethod
from src.models.mixins import LoggableMixin, SerializableMixin
from src.models.descriptors import PositiveNumber

# добавить валидацию, инициализацию. Буду использовать класс Payment, а то получается за каким хреном он тут у меня лежит и я отдельно передаю payment...для валидации дескриптор. По сути дескриптор бы переписать, что бы каждый раз не указывать имя _name, а сразу сделать на уровне дескриптора "_" + name...ладно, не забуду - сделаю.

class Payment:
    order_id = PositiveNumber("_order_id")
    amount = PositiveNumber("_amount")

    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount
        self.status = "pending"


class PaymentMethod(ABC):
    """Абстрактный класс для реализации методов оплаты"""

    @abstractmethod
    def process(self, payment: Payment):
        pass

    @abstractmethod
    def calculate_fee(self, payment: Payment):
        pass


class CardPayment(PaymentMethod, LoggableMixin, SerializableMixin):
    """Реализация оплаты картой с учетом комиссии"""

    def calculate_fee(self, payment: Payment)-> float:
        self.log(f"Расчет комиссии для CardPayment на сумму {payment.amount}")
        if payment.amount > 10000:
            return payment.amount * 0.02
        return payment.amount * 0.03

    def process(self, payment: Payment)-> bool:
        fee = self.calculate_fee(payment)
        result = payment.amount + fee
        payment.status = "completed"
        self.log(f"Оплата картой на сумму {result} успешно обработана")
        return True
    
    def to_json(self, payment: Payment):
        return {
            "type": "CardPayment",
            "fee": self.calculate_fee(payment),
            "amount": payment.amount
            }
    

class PaymentPayPal(PaymentMethod, LoggableMixin, SerializableMixin):
    """Реализация оплаты системой PayPal с учетом комиссии"""

    def calculate_fee(self, payment: Payment)-> float:
        self.log(f"Расчет комиссии для PayPal на сумму {payment.amount}")
        return payment.amount * 0.035

    # Логика для PayPal
    def process(self, payment: Payment)-> bool:
        fee = self.calculate_fee(payment)
        result = payment.amount + fee
        self.log(f"Оплата PayPal на сумму {result} успешно обработана")
        return True
    
    def to_json(self, payment: Payment):
        return {
            "type": "PaymentPayPal",
            "fee": self.calculate_fee(payment),
            "amount": payment.amount
            }


class BankTransfer(PaymentMethod, LoggableMixin, SerializableMixin):
    """Реализация банковского перевода с учетои комиссии"""

    def calculate_fee(self, payment: Payment)-> float:
        self.log(f"Расчет комиссии для банковского перевода на сумму {payment.amount}")
        return 50

    # Логика для банковского перевода
    def process(self, payment: Payment)-> bool:
        fee = self.calculate_fee(payment)
        result = payment.amount + fee
        self.log(f"Банковский перевод на сумму {result} успешно обработан")
        return True
    
    def to_json(self, payment: Payment):
        return {
            "type": "BankTransfer",
            "fee": self.calculate_fee(payment),
            "amount": payment.amount
            }