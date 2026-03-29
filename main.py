from sqlite3 import OperationalError
from src.database.connection import connect_to_db, get_user_by_id, create_user, create_order,get_user_orders


try:
    conn = connect_to_db("localhost", "sfmshop", "postgres", "DiggerLLP199222")


    if conn:
        try:
            user = create_user(conn, "Maria", "maria@test.com")
            print(user)
        except Exception as e:
            print(f"Ошибка добавления пользователя: {e}")


        user = get_user_by_id(conn, 63)
        print(f"Пользователь найден: {user}")


        try:
            order = create_order(conn, 63, 76500)
            print(order)
        except Exception as e:
            print(f"Ошибка: {e}")


        try:
            user_orders = get_user_orders(conn, 63)
            print("Заказы пользователя: ", end="")
            for order in user_orders:
                print(*order)
        except Exception as e:
            print(f"Ошибка: {e}")

    conn.close()
except OperationalError as e:
    print(f"Ошибка: {e}")

