from src.models.exceptions import BusinessLogicError
from src.models.product import Product


class DiscountRate:
    def __init__(self):
        self.discount = 0

    def get_discount(self, product):
        if not isinstance(product, Product):
            raise BusinessLogicError("Нет товара для расчета скидки")
        if product.price > 100_000:
            self.discount = 12
        elif  50_000 >= product.price <= 100_000:
            self.discount = 10
        elif product.price < 50_000:
            self.discount = 5
        return self.discount

