"""
TP1 - Exercice 4 : Classement des meilleures ventes
Use Case : Top produits ShopFast en temps réel
"""
import redis
from typing import Optional

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

KEY = "sales_rank"

def add_sale(r, pid, qty: int = 1):
    r.zincrby(KEY, qty, pid)

def get_top(r, limit: int = 10):
    res = r.zrevrange(KEY, 0, limit - 1, withscores=True)
    return [{"id": p, "val": s} for p, s in res]

def get_rank(r, pid):
    rk = r.zrevrank(KEY, pid)
    return rk + 1 if rk is not None else None

def get_range(r, low, high):
    return r.zrevrange(KEY, low - 1, high - 1)

if __name__ == "__main__":
    r.flushdb()
    for _ in range(10): add_sale(r, "prod_A", 2)
    print("Top:", get_top(r, 5))
    print("Rank A:", get_rank(r, "prod_A"))
