from src.models.exceptions import ValidationError
from src.database.connection import connect_to_db
from fastapi import HTTPException


class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        self.price = price
        if quantity < 0:
            raise ValidationError("Количество не может быть отрицательным")
        self.quantity = quantity

    # def set_price(self, price):
    #     if price < 0:
    #         raise ValidationError(f"Цена не может быть отрицательной")
    #     self.price = price

    def get_products_(conn, limit: int, offset: int):  # Вызываю функцию и передаю подключение к БД
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM products " \
                               "ORDER BY name DESC " \
                               "LIMIT %s OFFSET %s ", (limit, offset))  # Выполняю SQL-запрос для получения товаров из таблицы products количество ограничено limit и offset и сортирую по имени
                products = cursor.fetchall()  # Получаю все результаты запроса и сохраняю их в переменную products
                return products  
        except Exception as e:  
            raise ValidationError(f"Ошибка при получении товаров: {e}")  

    


    # def __str__(self):
    #     return f"Товар: {self.name}, Цена: {self.price}, Количество: {self.quantity}"

    # def __repr__(self):
    #     return f"Product: ('{self.name}', {self.price}, {self.quantity})"

    # def __lt__(self, other):
    #     return self.price < other.price

    # def __eq__(self, other):
    #     return self.price == other.price and self.price == other.price


    # def get_total_price(self):
    #   return self.price * self.quantity


    # def calculate_shipping(self):
    #     pass



    # def get_category(self):
    #     pass