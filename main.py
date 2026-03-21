from src.models.add_discount import DiscountRate
from src.models.exceptions import ValidationError
from src.models.product import Product


try:
    product = Product("Ноутбук", 50_000, 2)
    print(product)
except ValidationError as e:
    print(f"Ошибка: {e}")

try:
    discount = DiscountRate()
    print(discount.get_discount(product))
except ValidationError as e:
    print(f"Ошибка: {e}")