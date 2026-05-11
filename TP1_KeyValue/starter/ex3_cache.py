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


def get_product_cached(r, product_id: int, ttl: int = 600) -> Optional[dict]:
    start = time.time()
    cache_key = f"product_cache:{product_id}"
    cached = r.get(cache_key)
    if cached:
        product = json.loads(cached)
        elapsed = time.time() - start
        print(f"CACHE HIT ({elapsed * 1000:.2f}ms)")
        return product
    product = slow_db_get_product(product_id)
    if product:
        r.set(cache_key, json.dumps(product), ex=ttl)
    elapsed = time.time() - start
    print(f"CACHE MISS ({elapsed * 1000:.2f}ms)")
    return product


def invalidate_product_cache(r, product_id: int):
    r.delete(f"product_cache:{product_id}")


def benchmark_cache(r, product_id: int, iterations: int = 20):
    hits = 0
    misses = 0
    hit_time = 0.0
    miss_time = 0.0
    for _ in range(iterations):
        start = time.time()
        cache_key = f"product_cache:{product_id}"
        cached = r.get(cache_key)
        if cached:
            hit_time += time.time() - start
            hits += 1
        else:
            product = slow_db_get_product(product_id)
            if product:
                r.set(cache_key, json.dumps(product), ex=600)
            miss_time += time.time() - start
            misses += 1
    
    avg_hit = (hit_time / hits * 1000) if hits else 0.0
    avg_miss = (miss_time / misses * 1000) if misses else 0.0
    hit_rate = (hits / iterations) * 100
    
    print(f"Temps moyen cache HIT: {avg_hit:.2f}ms")
    print(f"Temps moyen cache MISS: {avg_miss:.2f}ms")
    print(f"Taux de cache hit: {hit_rate:.2f}%")


if __name__ == "__main__":
    r.flushdb()
    
    print("=== Test Cache-Aside ===")
    print("\nPremier appel (MISS attendu):")
    get_product_cached(r, 1)
    
    print("\nDeuxième appel (HIT attendu):")
    get_product_cached(r, 1)
    
    print("\n=== Benchmark ===")
    benchmark_cache(r, 1, iterations=10)
