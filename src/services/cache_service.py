import redis
import json
from src.database.queries import get_all_products_from_db, get_product
from random import randint
from datetime import datetime

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cached_products():
    cached = redis_client.get(f"products:all")
    if cached:
        print("Получено из кеша")
        return json.loads(cached)
    
    print(f"Получаю из БД и добавляю в кеш")
    products = get_all_products_from_db()
    redis_client.set(f"products:all", json.dumps(products))
    redis_client.expire(f"products:all", 3600)
    return products


# print(get_cached_products())

def get_cached_product(product_id):
    cached = redis_client.get(f"product:{product_id}")

    if cached:
        print("Получаю и кеша")
        return json.loads(cached)
    print("Получаю данные из БД")
    product = get_product(product_id)
    redis_client.setex(f"product:{product_id}", 3600, json.dumps(product))
    return product

# print(get_cached_product(1))

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

# print(create_user_session(2))

def get_user_session(session_token):
    session_key = f"session:{session_token}"
    cached = redis_client.get(session_key)
    if cached:
        print("Сессия открыта, получаю данные")
        return json.loads(cached)
    return None  # return f"Сессия не создана"

# print(get_user_session(6007))

def delete_user_session(session_token):
    session_key = f"session:{session_token}"
    redis_client.delete(session_key)
    return f"Удален токен {session_token}"

# print(delete_user_session(313))

