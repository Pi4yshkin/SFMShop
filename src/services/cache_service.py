import redis
import json
from src.database.queries import get_all_products_from_db

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


print(get_cached_products())