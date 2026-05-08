from src.database.connection import get_session
from src.database.models import User, Order, Product
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.services.cache_invalidation import invalidate_cache
# import logging

# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def get_user(user_id):
    session = get_session()
    try:
        user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        if user:
            return {"name": user.name, "email": user.email}
        return None
    except Exception as e:
        print("Ошибка: {e}")
        session.rollback()
    finally:
        session.close()


def get_all_users():
    session = get_session()
    try:
        values = session.execute(select(User)).scalars().all()
        users = []
        if values:
            for user in values:
                users.append(
                    {"id": user.id,
                    "name": user.name,
                    "email": user.email}
                )
            return users
        return []
    except Exception as e:
        print("Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# print(get_all_users())


def del_user(user_id):
    session = get_session()
    try:
        user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
        if user:
            session.delete(user)
            session.commit()
            invalidate_cache()  # удаляем из кеша
            return f'Пользователь {user.name} удален'
        return None
    except Exception as e:
        print("Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# print(del_user(2))

def get_user_orders(user_id):
    sessoin = get_session()
    try:
        user = sessoin.execute(select(User).where(User.id == user_id).options(joinedload(User.orders))).unique().scalar_one_or_none()
        if user:
            return [{"id": order.id, "total": float(order.total)} for order in user.orders]
        return []
    except Exception as e:
        print("Ошибка: {e}")
        sessoin.rollback()
    finally:
        sessoin.close()

# result = get_user_orders(3)
# print(result)


def create_order(user_id, total):
    session = get_session()
    try:
        order = Order(user_id = user_id, total = total)
        session.add(order)
        session.commit()
        # invalidate_cache()  # удаляю из кеша
        return order
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# create_order(3, 1500)

def create_user(name, email):
    session = get_session()
    try:
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        # invalidate_cache()  # удаляю из кеша
        return f"Пользователь {name} создан."
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# print(create_user("Виктория", "vika@test.com"))

def add_product_on_db(name, price, quantity):
    session = get_session()
    try:
        product = Product(name=name, price=price, quantity=quantity)
        session.add(product)
        session.commit()
        invalidate_cache("prodcts:all")  # удаляю из кеша
        return f"Добавлен продукт: {name}"
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# print(add_product_on_db("Mouse", 7500, 4))

def get_all_products_from_db():
    session = get_session()
    try:
        values = session.execute(select(Product)).scalars().all()
        products = []
        for product in values:
            products.append(
                {
                "name": product.name, 
                "price": float(product.price), 
                "quantity": product.quantity}
            )
        return products
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# print(get_all_products_from_db())


def update_name_product_in_db(product_id, new_name):
    session = get_session()
    try:
        product = session.execute(select(Product).where(Product.id == product_id)).scalar_one_or_none()
        if product:
            if new_name:
                product.name = new_name
                session.commit()
                invalidate_cache("products:all")  # удаляю из кеш
                return f"Название продукта успешно изменено на {new_name}"
            return f"Нет продукта с id {product_id}"
    except Exception as e:
        print(f"Ошибка: {e}")
        session.rollback()
    finally:
        session.close()

# print(update_name_product_in_db(1, "Ноутбук"))

