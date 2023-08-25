import redis

query = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

admin = 791927771
name = 'StudAIo'
api_url = 'http://127.0.0.1:7923'