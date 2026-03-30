import psycopg2
from src.database.connection import connect_to_db


def get_orders_with_products(conn, user_id):
    with conn.cursor() as cursor:
        cursor.execute("SELECT users.name, products.name, orders.total, order_items.quantity "
                       "FROM orders "
                       "INNER JOIN users ON orders.user_id = users.id "
                       "INNER JOIN order_items ON orders.id = order_items.order_id "
                       "INNER JOIN products ON order_items.product_id = products.id "
                       "WHERE users.id = %s ", (user_id,))
        orders = cursor.fetchall()
        return orders


def count_orders(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT users.name, COUNT(orders.id) "
                       "FROM users "
                       "INNER JOIN orders ON users.id = orders.user_id "
                       "GROUP BY users.name ")

        count_orders = cursor.fetchall()
        return count_orders


def sort_orders(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT users.name, orders.total, orders.created_at "
                       "FROM users "
                       "INNER JOIN orders ON users.id = orders.user_id "
                       "ORDER BY orders.total DESC ")
        orders = cursor.fetchall()
        return orders


