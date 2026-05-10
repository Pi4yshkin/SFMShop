from abc import ABC, abstractmethod
from src.models.user import User, UserValidator
from src.models.mixins import LoggableMixin


class CalculableItem(ABC):
    """Абстракция для получения общей суммы заказа"""
    @abstractmethod
    def get_totals(self):
        pass

    @abstractmethod
    def get_sum_totals(self):
        pass

    @abstractmethod
    def get_orders(self):
        pass

    @abstractmethod
    def len_orders(self):
        pass


class UserCalculator(CalculableItem):
    """Получение total из заказа"""
    def __init__(self, user: User):
        self.user = user

    def get_totals(self)-> list:
        total = [order["total"] for order in self.user.orders]
        return total
    
    def get_sum_totals(self):
        return sum(self.get_totals())
    
    def get_orders(self):
        total = [order for order in self.user.orders]
        return total
    
    def len_orders(self):  # возможно нужен магический метод __len__, но пока не понял как его реализовать для абстракции
        return len(self.get_orders())


class Database(ABC):
    """Абстрактный класс для реализации связи с БД"""
    @abstractmethod
    def save_to_db(self):
        pass


class SaveMySQL(Database):
    """Сохранение в PsQL"""
    def __init__(self, user: User):
        self.user = user

    def save_to_db(self)-> str:
        return f"Сохранение пользователя {self.user.user_id} в MySQL"


class NotificationService(ABC):
    """Абстрактный класс для реализации оповещений"""
    def send_notification(self):
        pass


class EmailNotification(NotificationService):
    """Сервис отправки уведомлений по email"""
    def __init__(self, user: User):
        self.user = user

    def send_notification(self)-> str:
        """Отправка приветственного email"""
        return f"Отправка email на {self.user.email}: Добро пожаловать, {self.user.name}!"
        

class DiscountStrategy(ABC):
    """Абстрактный класс для реализации принменения скидок"""
    def apply(self, balance: float):
        pass


class PercentDiscount(DiscountStrategy):
    """Применение процентной скидки"""
    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, balance: float)-> float:
        return balance * (1 + self.percent / 100)
    

class FixedDiscount(DiscountStrategy):
    """Применение фиксированной скидки"""
    def __init__(self, amount: float):
        self.amount = amount

    def apply(self, balance: float)-> float:
        return balance - self.amount


class UserService(LoggableMixin):
    """Бизнесс логика"""
    def __init__(self, user: User, user_calculator: UserCalculator, apply_discount: DiscountStrategy, send_message: NotificationService, save_to_db: Database):
        self.user = user
        self.user_calculator = user_calculator
        self.apply_discount = apply_discount
        self.send_message = send_message
        self.save_to_db = save_to_db

    def user_processor(self):
        print(f"Валидация: {UserValidator.validate_user(self.user)}")
        print(f"Потрачено: {self.user_calculator.get_sum_totals()}")
        print(f"Всего заказов: {self.user_calculator.len_orders()}")
        self.user.balance = self.apply_discount.apply(self.user.balance)
        print(f"Скидка для баланса: {self.user.balance:.2f}")
        print(self.send_message.send_notification())
        print(self.save_to_db.save_to_db())
        self.log(f"Заказ обработан {self.user.user_id}")
        return True