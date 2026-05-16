from src.database.queries import add_product_on_db, create_order, update_user, get_user_orders, del_user, get_all_products_from_db, get_product, create_user
from src.services.cache_service import get_cached_products, get_cached_product, get_cached_users, get_cached_one_user
from src.services.cache_invalidation import invalidate_cache


def queries_service():
    # print(add_product_on_db("GPU", 85000, 6))
    # print(add_product_on_db("Phone", 170000, 2))
    # print(add_product_on_db("Keyboard", 5000, 14))
    # print(add_product_on_db("Mouse", 3300, 7))
    # create_order(2, 12, 2)
    update_user(37, "email", "vika@test.com")  
    # print(get_user_orders(2))
    # print(del_user(2))
    # print(get_all_products_from_db())
    # print(get_product(12))
    # print(create_user("максим", "maks@test.com", 200000))

# if __name__ == "__main__":
#     queries_service()

def cached_service():
    # invalidate_cache('products:all')
    # print(get_cached_products())
    # print(get_cached_product(13))
    # print(get_cached_users())
    print(get_cached_one_user(35))


# if __name__ == "__main__":
#     cached_service()

