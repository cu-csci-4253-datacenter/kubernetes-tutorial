import redis

r = redis.Redis(host='localhost', port=6379)

for i in range(10):
    r.rpush("data", str(i))

print(r.lrange("data", 0,-1))
