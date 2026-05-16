import redis
import json
from src.services.cache_invalidation import invalidate_cache
from src.database.queries import get_all_products_from_db, get_product, get_all_users, get_user
from random import randint
from datetime import datetime

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cached_users():
    """Функция получения кеша/кеширования всех пользователей"""
    cached_all_users = redis_client.get('users:all')
    print(f"Проверка кеша")
    if cached_all_users:
        print(f"Получаю данные из кеша")
        return json.loads(cached_all_users)
    print(f"Кеш пуст, получаю данные из БД")
    users = get_all_users()
    print(f"Получены все пользователи")
    redis_client.setex('users:all', 3600, json.dumps(users))
    return users


def get_cached_one_user(user_id):
    """Функция получения кеша/кеширования пользователя по id"""
    cached_one_user = redis_client.get(f'user:{user_id}')
    if cached_one_user:
        print(f"Получаю данные из кеша")
        return json.loads(cached_one_user)
    print(f"Кеш пуст, получаю данные из БД")
    user = get_user(user_id)
    print(f"Получен пользователь с id: {user_id}")
    redis_client.setex(f'user:{user_id}', 3600, json.dumps(user))
    return user


def get_cached_products():
    cached = redis_client.get('products:all')
    print(f"Проверка кеша")
    if cached is None:
        print(f"Кеш пуст, очищаю перед получением свежих данных")
        invalidate_cache('products:all')

    if cached:
        print("Получено из кеша")
        return json.loads(cached)
    
    print(f"Получаю из БД и добавляю в кеш")
    products = get_all_products_from_db()
    redis_client.setex(f"products:all", 3600, json.dumps(products))
    return products

# def get_cached_products():
    # cached = redis_client.get('products:all')
    # print(f"Проверка кеша {cached}")
    # if cached is None:
    #     print(f"Кеш пуст, получаю из БД и добавляю в кеш")
    #     products = get_all_products_from_db()
    #     if products:
    #         redis_client.setex(f"products:all", 3600, json.dumps(products))
    #         print("Данные сохранены")
    #     return products

    # if cached:
    #     print("Получено из кеша")
    #     return json.loads(cached)
    

def get_cached_product(product_id):
    cached = redis_client.get(f"product:{product_id}")

    if cached:
        print("Получаю и кеша")
        return json.loads(cached)
    print("Получаю данные из БД")
    product = get_product(product_id)
    redis_client.setex(f"product:{product_id}", 3600, json.dumps(product))
    return product


def generate_token():
    """Генерация токена"""
    return randint(1000, 9999)


def create_user_session(user_id):
    session_token = generate_token()  # реализовал пока через модуль рандом. Скорее всего это не совсем верно, но на данный момент - работает
    session_data = {
        "user_id": user_id,
        "created_at": datetime.now().isoformat()
    }
    redis_client.setex(f"session:{session_token}", 86400, json.dumps(session_data))
    return f"Получен токен: {session_token}"


def get_user_session(session_token):
    session_key = f"session:{session_token}"
    cached = redis_client.get(session_key)
    if cached:
        print("Сессия открыта, получаю данные")
        return json.loads(cached)
    return None  # return f"Сессия не создана"


def delete_user_session(session_token):
    session_key = f"session:{session_token}"
    redis_client.delete(session_key)
    return f"Удален токен {session_token}"