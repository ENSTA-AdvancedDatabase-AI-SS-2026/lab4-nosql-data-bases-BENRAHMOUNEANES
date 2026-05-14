"""
TP1 - Exercice 1 : Structures de données Redis
Use Case : ShopFast - Gestion des produits, paniers et navigation
"""
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True)


def store_product(r, pid, data: dict):
    r.hset(f"item:{pid}", mapping=data)

def get_product(r, pid):
    res = r.hgetall(f"item:{pid}")
    return res if len(res) > 0 else None

def add_to_cart(r, uid, pid, qty: int = 1):
    r.hincrby(f"basket:{uid}", pid, qty)

def get_cart(r, uid):
    return r.hgetall(f"basket:{uid}")

def record_view(r, uid, pid, limit: int = 10):
    k = f"recent:{uid}"
    r.lpush(k, pid)
    r.ltrim(k, 0, limit - 1)

def get_history(r, uid):
    return r.lrange(f"recent:{uid}", 0, -1)

def add_product_to_category(r, cat: str, pid):
    r.sadd(f"tag:{cat}", pid)

def get_products_in_categories(r, *cats):
    tags = [f"tag:{c}" for c in cats]
    return r.sinter(tags) if tags else []

if __name__ == "__main__":
    r.flushdb()
    store_product(r, "p101", {"label": "Phone", "cost": "500"})
    add_to_cart(r, "u42", "p101", 1)
    print("Basket:", get_cart(r, "u42"))
    for x in ["p1", "p2", "p1"]: record_view(r, "u42", x)
    print("Recent:", get_history(r, "u42"))
