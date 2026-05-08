import time
from src.models.order import Order


def calculate_total(products):
    """Функция вычисления общей суммы товара на складе (не оптимизированно)"""
    total = 0
    for product in products:
        total += product[2] * product[3]
    return total


def calculate_total_with_sum(products):
    """Функция вычисления общей суммы товара на складе (оптимизированно)"""
    return sum(product[2] * product[3] for product in products)


def find_product_in_list(products, product_id):
    """Функция поиска элемента в списке по id (не оптимизированно O(n))"""
    for product in products:
        if product[0] == product_id:
            return product
    return None


def create_product_catalog(products):
    """Функция создания словаря из списка"""
    return {product[0]: product for product in products}


def find_product_in_dict(products, product_id):
    """Функция получения элемента по ключу из словаря, созданного из списка (оптиизированно O(1))"""
    return products.get(product_id, None)


def benchmark_serch(products, product_id):
    """Функция рассчета ускорения времени работы функций поиска элемента по спису и словарю"""
    start_time = time.time()
    result_list = find_product_in_list(products, product_id)
    end_time = time.time()
    time_list = end_time - start_time

    product_dict = create_product_catalog(products)
    start_time = time.time()
    result_dict = find_product_in_dict(product_dict, product_id)
    end_time = time.time()
    time_dict = end_time - start_time

    speedup = time_list / time_dict if time_dict > 0 else 0
    return {
            "time_list": {time_list},
            "time_dict": {time_dict},
            "speedup": {speedup}
            } 


def benchmark_cnt_total(products):
    """Функция рассчета ускорения времени работы функций подсчета вычисления общей суммы товара на складе"""
    start_time = time.time()
    res_total = calculate_total(products)
    end_time = time.time()
    time_total = end_time - start_time

    start_time = time.time()
    res_total_with_sum = calculate_total_with_sum(products)
    end_time = time.time()
    time_total_with_sum = end_time - start_time

    speedup = time_total / time_total_with_sum if time_total_with_sum > 0 else 0

    return {
            "time_total": {time_total},
            "time_total_with_sum": {time_total_with_sum},
            "speedup": {speedup}
           }


