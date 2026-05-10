from abc import ABC, abstractmethod
from src.models.order import Order
from src.models.mixins import LoggableMixin
from src.models.exceptions import ValidationError



class OrderValidator:

    @staticmethod
    def validate(order: Order) -> bool:
        if not isinstance(order.order_id, int):
            raise ValidationError("id должен быть числом")
        if not order.items:
            raise ValidationError("Заказ не может быть пустым")
        if not order.user:
            raise ValidationError("У заказа должен быть пользователь")
        return True


class OrderCalculator:
    """Расчет суммы с уже примененной скидкой"""
    @staticmethod
    def calculate_total(discount: DiscountStrategy, order: Order) -> float:
        total = sum(item.calculate_subtotal() for item in order.items)
        return discount.apply(total)
    
class CalculableItem(ABC):
    """Абстракция для рассчета промежуточной стоимости товара"""
    def calculate_subtotal(self):
        pass


class PhysicalProduct(CalculableItem):
    """Рассчет промежуточной стоимости товаров с полями price и quantity (убираем жесткую зависимость высокоуровневых модулей от низкоуровневых)"""
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity

    def calculate_subtotal(self):
        return self.price * self.quantity


class DiscountStrategy(ABC):
    """Абстрактный класс для реализации скидок"""
    @abstractmethod
    def apply(self, price: float):
        pass


class PercentDiscount(DiscountStrategy):
    """Расчет скидки с учетом процента"""
    def __init__(self, percent: float) -> float:
        if not isinstance(percent, (int, float)):
            raise ValidationError(f"Процент должен быть числом")
        self.precent = percent

    def apply(self, price: float) -> float:
        return price * (1 - self.precent / 100)
    
    def __str__(self):
        return f"{self.apply}%"
    

class FixedDiscount(DiscountStrategy):
    """Расчет скидки с учетом фиксированной суммы"""
    def __init__(self, amount: float) -> float:
        if not isinstance(amount, (int, float)):
            raise ValidationError(f"Сумма скидки должна быть числом")
        self.amount = amount

    def apply(self, price: float) -> float:
        return price - self.amount
    
    def __str__(self):
        return f"{self.apply} руб."


class Database(ABC):
    """Абстрактный класс реализаций сохранения информации о платеже в различные БД"""

    @abstractmethod
    def save_to_database(self):
        pass


class SavePsQL(Database):

    def __init__(self, order: Order):
        self.order = order
    
    def save_to_database(self):
        """Сохранение в БД"""
        print(f"Сохранение платежа. ID: {self.order.order_id} в PsQL")


class NotificationService(ABC):
    """Абстрактный класс для реализации отправки уведомлений"""
    @abstractmethod
    def send_notification(self):
        pass


class EmailNotifical(NotificationService):
    """Класс для отправки уведомлений по email"""
    def __init__(self, order: Order):
        self.order = order

    def send_notification(self):
        """Отправка уведомления"""
        print(f"Отправка email. ID: {self.order.order_id}")


class OrderServices(LoggableMixin):
    
    def __init__(self, order: Order, discount: DiscountStrategy, repository: Database, notification: NotificationService):
        self.order = order
        self.discount = discount
        self.repository = repository
        self.notification = notification

    def order_process(self):

        print(OrderCalculator.calculate_total(self.discount, self.order))

        self.repository.save_to_database()

        self.notification.send_notification()

        self.log(f"Заказ обработан. ID: {self.order.order_id}")
