import redis


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def invalidate_cache(*args):
    print("Удаляю из кеша")
    redis_client.delete(args)