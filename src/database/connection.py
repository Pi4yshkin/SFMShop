import psycopg2
from psycopg2 import errors, OperationalError


def connect_to_db(host, database, user, password):
    try:
        conn = psycopg2.connect(host=host,
                              database=database,
                              user=user,
                              password=password)
        return conn
    except OperationalError as e:
        print(f"Ошибка подключения к БД: {e}")
        raise



def add_product(conn, name, price, quantity):
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)", (name, price, quantity))
        print(f"Товар добавлен: {name}, {price}, {quantity}")
        conn.commit()

def get_products(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM products")

        products = cursor.fetchall()
        return products


def update_product_price(conn, product_id, new_price):
    with conn.cursor() as cursor:
        cursor.execute("UPDATE products SET price = %s WHERE id = %s", (new_price, product_id))
        print(f"Цена обновлена: {new_price}")
        conn.commit()


def create_user(conn, name, email):
    with conn.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
            conn.commit()
            return f"Пользователь создан: {name}, {email}"
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            raise Exception(f"Такой email уже существует!")


def get_user_by_id(conn, user_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id, ))
        user = cursor.fetchone()
        if user:
            return dict(id=user[0], name=user[1], email=user[2])
        else:
            return None


def create_order(conn, user_id, total):
    with conn.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO orders (user_id, total) VALUES (%s, %s)", (user_id, total))
            conn.commit()
            return f"Заказа создан: user_id={user_id}, total={total}"
        except errors.ForeignKeyViolation:
            conn.rollback()
            raise Exception(f"Пользователя не существует")


def get_user_orders(conn, user_id):
    if get_user_by_id(conn, user_id):
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE user_id = %s", (user_id, ))
            orders = cursor.fetchall()
            return orders
    else:
        conn.rollback()
        raise Exception(f"Пользователя с id {user_id} не существует")


def add_order_in_order_items(conn, order_id, product_id, quantity):
    with conn.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO order_items (order_id, product_id, quantity) VALUES (%s, %s, %s)",
                           (order_id, product_id, quantity))
            conn.commit()
        except errors.ForeignKeyViolation:
            conn.rollback()
            raise Exception(f"Заказ не найден!")

