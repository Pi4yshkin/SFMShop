import redis


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def invalidate_cache(cached_key):
    print("Удаляю из кеша")
    redis_client.delete(cached_key)