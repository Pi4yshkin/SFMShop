from src.database.connection import connect_to_db, get_user_by_id
from src.database.connection import create_user
from src.database.connection import create_order
from src.database.connection import get_user_orders

conn = connect_to_db("localhost", "sfmshop", "postgres", "DiggerLLP199222")


try:
    user = create_user(conn, "Alex", "alex@test.com")
    print(user)
except Exception as e:
    print(f"Ошибка добавления пользователя: {e}")


user = get_user_by_id(conn, 4)
print(f"Пользователь найден: {user}")


try:
    order = create_order(conn, 4, 76500)
    print(order)
except Exception as e:
    print(f"Ошибка: {e}")

try:
    user_orders = get_user_orders(conn, 4)
    print("Заказы пользователя: ", end="")
    for order in user_orders:
        print(*order)
except Exception as e:
    print(f"Ошибка: {e}")