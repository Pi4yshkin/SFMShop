from src.models.exceptions import ValidationError, BusinessLogicError
from src.models.product import Product
from src.models.user import User
from src.database.connection import connect_to_db
from fastapi import FastAPI, HTTPException


class Order:
    # def __init__(self, user, products):
    #     if not isinstance(user, User):
    #         raise ValidationError("Пользователя не существует")
    #     self.user = user
    #     if not products:
    #         raise BusinessLogicError("Список товаров пуст")
    #     self.products = list(products)
    #     self.total = 0

    # def add_product(self, product):
    #     if not isinstance(product, Product):
    #         raise ValidationError("Заказ не существует")
    #     self.products.append(product)
    #     return self.products

    def add_order(conn, user_id, total):
        try:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s)", (user_id, total))
                if cursor.rowcount <= 0:
                    raise HTTPException(status_code=400, detail="Неверный формат данных")
                conn.commit()
        except Exception as e:
            raise e

        
    # def calculate_total(self):
    #     for product in self.products:
    #         self.total += product.price * product.quantity
    #     return self.total

    # def __str__(self):
    #     return f"Заказ пользователя {self.user.name} на сумму {self.total} руб."