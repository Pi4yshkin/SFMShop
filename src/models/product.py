from src.models.exceptions import ValidationError
# from src.models.add_discount import DiscountRate


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self.price = price
        if quantity < 0:
            raise ValidationError("Количество не может быть отрицательным")
        self.quantity = quantity

    def set_price(self, price):
        if price < 0:
            raise ValidationError(f"Цена не может быть отрицательной")
        self.price = price

    def __str__(self):
        return f"Товар: {self.name}, Цена: {self.price}, Количество: {self.quantity}"

    def __repr__(self):
        return f"Product: ('{self.name}', {self.price}, {self.quantity})"

    def __lt__(self, other):
        return self.price < other.price

    def __eq__(self, other):
        return self.price == other.price and self.price == other.price


    def get_total_price(self):
        return self.price * self.quantity

    def calculate_shipping(self):
        pass

    