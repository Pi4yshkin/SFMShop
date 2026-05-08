from src.models.exceptions import ValidationError
from abc import ABC, abstractmethod
from src.models.mixins import LoggableMixin, SerializableMixin
from src.models.metaclasses import ModelMeta
from src.models.descriptors import PositiveNumber, CachedProperty


class Product(LoggableMixin, SerializableMixin, metaclass=ModelMeta):
    price = PositiveNumber("_price")  # дескриптор проверки
    quantity = PositiveNumber("_quantity")  # дескриптор проверки

    """Класс для хранения заказа"""
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.log(f"Продукт создан: {name}")

    def __contains__(self, item):
        return item in self.name

    # @property реализован через дестриптор, имеет метод __get__, .setter имеет метод __set__. Дескриптор PositiveNumber в отличии от property компактный, не требует создания методов для каждого атрибута. Можно импортировать в любой класс.
    # @property
    # def price(self):
    #     return self._price
    
    # @price.setter
    # def price(self, value):
    #     if value <= 0:
    #         raise ValidationError("Цена должна быть положительной")
    #     self._price = value

    # @property
    # def quantity(self):
    #     return self._quantity
    
    # @quantity.setter
    # def quantity(self, value):
    #     if value < 0:
    #         raise ValidationError("Количество не может быть отрицательным")
    #     self._quantity = value

    # def __str__(self):
    #     return f"наименование: {self.name}, цена: {self.price}, кол-во: {self.quantity}"
    
    def __repr__(self):
        return f"наименование: {self.name}, цена: {self.price}, кол-во: {self.quantity}"


class ProductCalculator:

    def __init__(self, product: Product):
        self.product = product

    """Метод применения скидки"""
    def calculate_price_with_discount(self, discount: DiscountStrategy) -> float:
        return discount.apply(self.product.price)

    """Метод рассчета общей суммы на товар, если кол-во > 1"""
    @CachedProperty
    def calculate_total_value(self) -> float:
        print("Вычисляю...")
        if self.product.quantity > 1:
            return self.product.price * self.product.quantity
        return self.product.price



class ProductValidate:
    """Валидация данных"""
    def validate(product: Product) -> bool:
        if not isinstance(product.name, str):
            raise ValidationError("Наименование должно быть строкой")
    
            

class DiscountStrategy(ABC):
    """Абстрактный класс для реализации скидок"""
    @abstractmethod
    def apply(price: float) -> float:
        pass


class PercentDiscount(DiscountStrategy):
    """Расчет скидки с учетом процента"""
    def __init__(self, precent: float) -> float:
        if not isinstance(precent, (int, float)):
            raise ValidationError(f"Процент должен быть числом")
        self.precent = precent

    def apply(self, price: float) -> float:
        return price * (1 - self.precent / 100)


class FixedDiscount(DiscountStrategy):
    """Расчет скидки с учетом фиксированной суммы"""
    def __init__(self, amount: float) -> float:
        if not isinstance(amount, (int, float)):
            raise ValidationError(f"Сумма скидки должна быть числом")
        self.amount = amount

    def apply(self, price: float) -> float:
        return price - self.amount