import redis

r = redis.Redis(port=18401, decode_responses=True)

r.set("greeting", "hello")
print(r.get("greeting"))
print(r.incr("visits"), r.incr("visits"))
r.set("session:abc", "lukas", ex=30)
print(r.get("session:abc"), r.ttl("session:abc"))
r.hset("course:1", mapping={"title": "Python Basics", "price": 499})
print(r.hgetall("course:1"))
print(r.get("missing"))
