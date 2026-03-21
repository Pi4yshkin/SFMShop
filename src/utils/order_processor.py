def load_orders_from_file(filename):
    orders = []  # список для строк заказаов
    try:
        with open("../data/orders.txt", "r") as file:
            for line in file.readlines():
                line = line.strip().split(":")
                orders.append(line)
            return orders
    except FileNotFoundError:
        print("Файл order.txt не найден")
        return []


def calculate_order_total(price, discount_rate):
    return round(price * (1 - discount_rate), 2)


def get_discount_by_total(total):
    if total <= 0:
        return 0
    elif total > 10_000:
        discount_rate = 0.15
    elif total > 5000:
        discount_rate = 0.10
    else:
        discount_rate = 0.05
    return discount_rate


def process_orders(orders_data):
    lst_order_dict = []  # список со словарями заказов
    for order in orders_data:
        dict_order = {} # для каждой итерации создается новый словарь,
        # иначе получим список словарей из последней обработанной строки
        dict_order["order_id"] = order[0]
        try:
            price = int(order[1])  # создал переменную, что бы проще и читабельнее было в расчете dict["total"]
            dict_order["total"] = calculate_order_total(price, get_discount_by_total(price))
        except ValueError:
            print(f"Неверный формат суммы")
            continue
        try:
            if order[2] == "новый" or order[2] == "обработан":
                dict_order["status"] = order[2]
        except ValueError:
            print(f"Неверный формат статуса заказа")
            continue
        dict_order["user"] = order[3]
        lst_order_dict.append(dict_order)
    return lst_order_dict


def analyse_orders(processed_orders):
    stats = {}
    total_sum = 0  # счетчик общей суммы заказов
    cnt_1 = 0  # счетчик для статуса "новый"
    cnt_2 = 0  # счетчик для статуса "обработан"
    unique_set = set()
    for order in processed_orders:
        try:
            total_sum += order["total"]
        except ValueError:
            print(f"Неверный формат цены товара")
            continue
        stats["total_orders"] = len(processed_orders)
        stats["total_sum"] = total_sum
        stats["by_status"] = {}
        try:
            if order["status"] not in stats["by_status"]:
                if order["status"] == "новый":
                    cnt_1 += 1
                stats["by_status"].update({"новый": cnt_1})
                if order["status"] == "обработан":
                    cnt_2 += 1
                stats["by_status"].update({"обработан": cnt_2})
        except KeyError:
            print(f"Неверный формат статуса заказа")
            continue
        unique_set.add(order["user"])
        stats["unique_users"] = list(unique_set)
    return stats
