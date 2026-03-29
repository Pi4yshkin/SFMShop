import psycopg2
from src.database.connection import connect_to_db


# def get_orders_with_products(conn, user_id):
#     with conn.cursor() as cursor:
#         cursor.execute("SELECT orders.id, users.name, products.total"
#                        "FROM orders"
#                        "INNER JOIN users ON orders.user_id = %s", (user_id,))
#         orders = cursor.fetchall()
#         return orders



