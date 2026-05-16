import redis


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def invalidate_cache(*args):
    print(f"Удаляю из кеша ключи {args}")
    redis_client.delete(*args)
    print(f"Кеш очищен")

# invalidate_cache("product:all")