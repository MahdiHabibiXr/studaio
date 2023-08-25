import redis

query = redis.StrictRedis(
    host='redis.studaio.svc',
    port=6379,
    password='lHsXtUaX2bK4J0G36uKVaLfoz9KyyeBJ'
    db=0,
    decode_responses=True
)

admin = 791927771
name = 'StudAIo'