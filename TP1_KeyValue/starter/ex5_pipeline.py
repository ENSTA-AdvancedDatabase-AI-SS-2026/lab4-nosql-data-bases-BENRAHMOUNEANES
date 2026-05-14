"""
TP1 - Exercice 5 : Pipeline & Transactions
Use Case : ShopFast - Insertion en masse et achats atomiques
"""
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def batch_load(r, data: list):
    with r.pipeline() as p:
        for d in data:
            p.hset(f"product:{d['id']}", mapping=d)
        p.execute()

def process_checkout(r, uid):
    k = f"cart:{uid}"
    r.watch(k)
    if not r.exists(k):
        r.unwatch()
        return False
    with r.pipeline(transaction=True) as p:
        p.delete(k)
        p.execute()
    return True

if __name__ == "__main__":
    r.flushdb()
    batch_load(r, [{"id": "1", "name": "A"}, {"id": "2", "name": "B"}])
    r.hset("cart:u1", "1", "1")
    print("Done:", process_checkout(r, "u1"))
