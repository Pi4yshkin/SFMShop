from src.models.exceptions import ValidationError, BusinessLogicError
from src.models.product import Product
from src.models.user import User


class Order:
    def __init__(self, user, products):
        if not isinstance(user, User):
            raise ValidationError("Пользователя не существует")
        self.user = user
        if not products:
            raise BusinessLogicError("Список товаров пуст")
        self.products = list(products)
        self.total = 0

    def add_product(self, product):
        if not isinstance(product, Product):
            raise ValidationError("Заказ не существует")
        self.products.append(product)
        return self.products

    def calculate_total(self):
        for product in self.products:
            self.total += product.price * product.quantity
        return self.total

    def __str__(self):
        return f"Заказ пользователя {self.user.name} на сумму {self.total} руб."