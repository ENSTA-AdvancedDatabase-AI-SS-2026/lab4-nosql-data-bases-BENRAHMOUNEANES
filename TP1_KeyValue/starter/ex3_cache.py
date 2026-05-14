"""
TP1 - Exercice 3 : Pattern Cache-Aside avec TTL
Use Case : Cache des pages produits ShopFast
"""
import redis
import json
import time
from typing import Optional

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def slow_db_get_product(product_id: int) -> Optional[dict]:
    """Simule une requête PostgreSQL lente (2 secondes)"""
    time.sleep(2)
    products = {
        1: {"id": 1, "name": "Samsung Galaxy A54", "price": 65000, "stock": 15},
        2: {"id": 2, "name": "Laptop HP 15-inch", "price": 120000, "stock": 8},
        3: {"id": 3, "name": "Casque JBL Bluetooth", "price": 12000, "stock": 50},
        4: {"id": 4, "name": "Clavier Mécanique", "price": 8000, "stock": 30},
    }
    return products.get(product_id)


def get_product_cached(r, pid: int, exp: int = 600) -> Optional[dict]:
    t0 = time.time()
    k = f"cache:prod:{pid}"
    data = r.get(k)
    
    if data:
        ms = (time.time() - t0) * 1000
        print(f"HIT [{ms:.2f}ms]")
        return json.loads(data)
    
    item = slow_db_get_product(pid)
    if item:
        r.setex(k, exp, json.dumps(item))
    
    ms = (time.time() - t0) * 1000
    print(f"MISS [{ms:.2f}ms]")
    return item

def clear_cache(r, pid: int):
    r.delete(f"cache:prod:{pid}")

def run_bench(r, pid: int, count: int = 20):
    stats = {"hits": 0, "misses": 0}
    for _ in range(count):
        k = f"cache:prod:{pid}"
        if r.get(k): stats["hits"] += 1
        else:
            p = slow_db_get_product(pid)
            if p: r.setex(k, 600, json.dumps(p))
            stats["misses"] += 1
    print(f"Stats: {stats}")

if __name__ == "__main__":
    r.flushdb()
    get_product_cached(r, 1)
    get_product_cached(r, 1)
    run_bench(r, 2, 5)
