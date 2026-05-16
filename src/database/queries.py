from src.database.connection import get_session
from src.database.models import User, Order, Product, OrderItems
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from src.services.cache_invalidation import invalidate_cache
from src.models.descriptors import PositiveNumber
import time
# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_user(user_id):
    """Функция получения пользователя по id из таблицы users"""
    with get_session(True) as session:
        try:
            user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
            if user:
                return {"name": user.name, "email": user.email, "balance": float(user.balance)}
            return None
        except Exception as e:
            print(f"Ошибка: {e}")


def get_all_users():
    """Функция получения всех пользователей из таблицы users"""
    with get_session(True) as session:
        try:
            values = session.execute(select(User)).scalars().all()
            users = []
            if values:
                for user in values:
                    users.append(
                        {"id": user.id,
                        "name": user.name,
                        "email": user.email,
                        "balance": float(user.balance)}
                    )
                return users
            return []
        except Exception as e:
            print(f"Ошибка: {e}")

def update_user(user_id, field, value):
    """Обновление данных пользователя. Необходимо передать id, поле которое необходимо изменить и значение"""

    with get_session(False) as session:
        try:
            invalidate_cache(f'user:{user_id}')  # удаляю кеш перед изменением данных

            user = select(User).where(User.id == user_id).with_for_update()

            # compiled = user.compile(compile_kwargs={"literal_binds": True})  # проверю на пополнении баланса
            # explain_sql = f"EXPLAIN ANALYZE {str(compiled)}"
            # explained = session.execute(text(explain_sql))
            # for row in explained:
            #     print(row[0])

            # Planning Time: 0.588 ms
            # Execution Time: 0.113 ms

            user = session.execute(user).scalar_one_or_none()
            print("Проверяю, существует ли пользователь")
            if not user:
                raise ValueError(f"Пользователь с id: {user_id} не найден")
            print(f"Пользователь существует. Проверяю, есть ли у пользователя нужное поле для изменения")
            if not hasattr(user, field):
                raise ValueError(f"У пользователя отсутствует поле {field}")
            print(f"Поле существует")
            print(f"Проверяю буду ли я изменять баланс пользователя")
            if field == "balance":  # если изменять буду баланс, например, пополнение счета, то к старому значению прибавлю новое
                print(f"Верно, буду изменять поле баланса")
                if isinstance(value, (int, float)) and value > 0:
                    user.balance += value
                    return f"Баланс пользователя {user.name} пополнен на {value} руб."
            print(f"Нет, изменять буду другое поле")
            if field == "email":
                check_unique_email = session.execute(select(User).where(User.email == value)).scalar_one_or_none()
                if check_unique_email:
                    if check_unique_email and check_unique_email.id != user_id:
                        raise ValueError(f"Такой email уже используется")
                setattr(user, field, value)  # остальные поля заменяю на новое значение целиком
                print(f"Поле изменено")
                return user
        
            setattr(user, field, value)  # остальные поля заменяю на новое значение целиком
            print(f"Поле изменено")
            return user
        
        except IntegrityError as e:
            print("Откат транзакции")
            session.rollback()
            return f"Ошибка: такой email {value} уже используется"
        except Exception as e:
            print(f"Ошибка: {e}")
            print(f"Откат транзакции")
            session.rollback()



def del_user(user_id):
    """Функция удаления пользователя по id"""

    with get_session(False) as session:
        try:
            invalidate_cache(f'user:{user_id}')  # удаляю пользователя из кеша

            user = select(User).where(User.id == user_id)  # создаю объект

            # compiled = user.compile(compile_kwargs={"literal_binds": True})  # compile() - превращаю объект в SQL запрос, compile_kwargs={"literal_binds": True} - создает запрос без плейсхолдеров. Опасно для обычных запросов, только для EXPLAIN ANALYZE. 
            # explain_sql = f"EXPLAIN ANALYZE {str(compiled)}" # "EXPLAIN ANALYZE SELECT users.id, users.name FROM users WHERE users.id = 5"
            # explained = session.execute(text(explain_sql))  # text() переводит строку в SQL выражение
            # for row in explained:
            #     print(row[0])

            # Planning Time: 0.248 ms
            # Execution Time: 0.023 ms

            user = session.execute(user).scalar_one_or_none()

            if user:
                session.delete(user)
                # invalidate_cache('')  # удаляем из кеша
                return f'Пользователь {user.name} удален'
            return None
        except Exception as e:
            print(f"Ошибка: {e}")
            session.rollback()


def get_user_orders(user_id):
    """Функция получения заказов пользователя по его id"""

    with get_session(True) as session:
        try:
            stmt = select(User).where(User.id == user_id).options(joinedload(User.orders))

            # compiled = stmt.compile(compile_kwargs={"literal_binds": True})
            # explain_sql = f"EXPLAIN ANALYZE {str(compiled)}"
            # explained = session.execute(text(explain_sql))
            # for row in explained:
            #     print(row[0])

            # Planning Time: 1.314 ms
            # Execution Time: 0.046 ms

            user = session.execute(stmt).unique().scalar_one_or_none()

            if user:
                return [{"id": order.id, "total": float(order.total)} for order in user.orders]
            return []
        except Exception as e:
            print(f"Ошибка: {e}")


def create_order(user_id, product_id, quantity):
    """Функция создания заказа для пользователя"""

    PositiveNumber("quantity")(quantity)

    with get_session(False) as session:
        try:
            print("Удаляю кеш перед добавлением заказа")
            invalidate_cache('products:all', 'users:all')

            product = session.get(Product, product_id)
            if product:
                if product.stock < quantity:
                    raise ValueError("Недостаточно товара на складе")
            print("Товара достаточно")
            product.stock -= quantity  # проверяю, хватает ли товара на складе

            total = product.price * quantity  # вычисляю, сколько пользователь заплатит за товар
            print(f"Стоимость заказа {total}")

            user = session.execute(select(User).where(User.id == user_id).with_for_update()).scalar_one_or_none()  # получаю пользователя для проверки хватает ли у него средст для оплаты
            if not user:
                raise ValueError(f"Пользователь с id: {user_id} не найден")
            if user.balance < total: 
                raise ValueError(f"Недостаточно средст у пользователя {user.name}")
                
            print(f"Денег у пользователя хватает, списываю")
            user.balance -= total

            order = Order(user_id=user_id, total=total)
            order.status = "completed"
            session.add(order)
            session.flush()  # получить id

            order_items = OrderItems(order_id=order.id, product_id=product.id, quantity=quantity, price=product.price)
            session.add(order_items)

            return f"{order}"
        
        except Exception as e:
            print(f"Ошибка: {e}")
            print(f"Откат транзакции")
            session.rollback()


def create_user(name, email, balance):
    """Функция создания пользователя с валидацией баланса и email"""

    PositiveNumber("balance")(balance)

    with get_session(False) as session:
        try:
            invalidate_cache('users:all')  # удаляю из кеша
            user = User(name=name, email=email, balance=balance)
            session.add(user)
            session.flush()
            return f"Пользователь {name} создан."
        except IntegrityError as e:
            print("Откат транзакции")
            session.rollback()
            return ValueError("Пользователь с таким email уже существует")
        except Exception as e:
            print(f"Ошибка: {e}")
            print("Откат транзакции")
            session.rollback()


def add_product_on_db(name, price, quantity):
    """Функция добавления товара в БД"""

    PositiveNumber("quantity")(quantity)

    with get_session(False) as session:
        try:
            invalidate_cache("products:all")
            product = Product(name=name, price=price, stock=quantity)
            session.add(product)
            return f"Добавлен продукт: {name}"
        except Exception as e:
            print(f"Ошибка: {e}")
            session.rollback()


def get_all_products_from_db():
    """Функция для получения всех товаров из таблицы products"""

    with get_session(True) as session:
        try:
            values = select(Product)

            # compiled = values.compile(compile_kwargs={"literal_binds": True})
            # explain_sql = f"EXPLAIN ANALYZE {str(compiled)}"
            # explain = session.execute(text(explain_sql))
            # for row in explain:
            #     print(row[0])

            # Planning Time: 0.295 ms
            # Execution Time: 0.019 ms

            values = session.execute(values).scalars().all()

            products = []
            for product in values:
                products.append(
                    {
                    "name": product.name, 
                    "price": float(product.price), 
                    "stock": product.stock}
                )
            return products
        except Exception as e:
            print(f"Ошибка: {e}")


def get_product(product_id):
    """Функция получения товара по его id"""

    with get_session(True) as session:
        try:
            product = select(Product).where(Product.id == product_id)

            # compiled = product.compile(compile_kwargs={"literal_binds": True})
            # explain_sql = f"EXPLAIN ANALYZE {str(compiled)}"
            # explained = session.execute(text(explain_sql))
            # for row in explained:
            #     print(row[0])

            # Planning Time: 0.286 ms
            # Execution Time: 0.022 ms

            product = session.execute(product).scalar_one_or_none()

            return f"product_name: {product.name} price: {product.price} stock: {product.stock}"
        except Exception as e:
            print(f"Ошибка: {e}")
