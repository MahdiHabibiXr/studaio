import redis

query = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

admin = 791927771
name = 'StudAIo'