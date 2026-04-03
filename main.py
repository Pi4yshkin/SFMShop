import psycopg2
from psycopg2 import OperationalError
from src.database.connection import (connect_to_db, get_user_by_id, create_user, get_all_products,
                                     create_order,get_user_orders, add_order_in_order_items, add_product_in_stock, delete_order)
from src.database.queries import get_user_order_history, get_order_statistics, get_top_products

def main():
    try:
        conn = connect_to_db("localhost", "sfmshop", "postgres", "DiggerLLP199222")


        if conn:
            try:
                user = create_user(conn, "Alena", "alena@test.com")
                print(user)
            except Exception as e:
                print(f"Ошибка добавления пользователя: {e}")
            
            
            try:
                products = get_all_products(conn)
                for product in products:
                    print(*product)
                print()
            except Exception as e:
                print(f"Ошибка: {e}")
            #
            try:
                user = get_user_by_id(conn, 4)
                print(user)
                print()
            except Exception as e:
                print(f"Ошибка: {e}")
            #
            # try:
            #     add_product = add_product_in_stock(conn, "Светильник", 12_000, 3)
            #     print(add_product)
            # except Exception as e:
            #     print(f"Ошибка: {e}") 
            #
            # try:
            #     order = create_order(conn, 1, 95_000)
            #     print(order)
            # except Exception as e:
            #     print(f"Ошибка: {e}")
            #
            #
            # try:
            #     user_orders = get_user_orders(conn, 63)
            #     print("Заказы пользователя: ", end="")
            #     for order in user_orders:
            #         print(*order)
            # except Exception as e:
            #     print(f"Ошибка: {e}")

            # orders = get_orders_with_products(conn, 63)
            # print(orders)

            # try:
            #     add_order_in_order_items(conn, 4, 2, 1)
            # except Exception as e:
            #     print(f"Ошибка: {e}")


            # orders = get_orders_with_products(conn, 63)
            # for order in orders:
            #     print(*order)

            # orders = count_orders(conn)
            # print(orders)
            #
            # sorted_orders = sort_orders(conn)
            # for order in sorted_orders:
            #     print(*order)

            try:
                orders_history = get_user_order_history(conn, 4)
                for order in orders_history:
                    print(*order)
                print()
            except Exception as e:
                print(f"Ошибка: {e}")

            try:
                orders_statistics = get_order_statistics(conn)
                for order in orders_statistics:
                    print(*order)
                print()
            except Exception as e:
                print(f"Ошибка: {e}")

            try:
                top_products = get_top_products(conn)
                for product in top_products:
                    print(*product)
                print()
            except Exception as e:
                print(f"Ошибка: {e}")


            # try:
            #     res_del = delete_order(conn, 2)
            #     print(res_del)
            # except Exception as e:
            #     print(f"Ошибка: {e}")

        conn.close()
    except OperationalError as e:
        print(f"Ошибка: {e}")

main()