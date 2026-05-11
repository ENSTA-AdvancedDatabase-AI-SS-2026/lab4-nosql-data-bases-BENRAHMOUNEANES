"""
TP1 - Exercice 5 : Pipeline & Transactions
Use Case : ShopFast - Insertion en masse et achats atomiques
"""
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def bulk_insert_products(r, products: list):
    """Bulk insert avec pipeline pour maximiser le débit"""
    pipe = r.pipeline()
    for p in products:
        pipe.hset(f"product:{p['id']}", mapping=p)
    pipe.execute()

def checkout_cart(r, user_id: str):
    """Transaction MULTI/EXEC pour valider le panier de façon atomique"""
    cart_key = f"cart:{user_id}"
    
    r.watch(cart_key)
    cart = r.hgetall(cart_key)
    
    if not cart:
        r.unwatch()
        return False
        
    pipe = r.pipeline(transaction=True)
    pipe.delete(cart_key)
    pipe.execute()
    return True

if __name__ == "__main__":
    r.flushdb()
    products = [
        {"id": "1", "name": "Samsung Galaxy A54", "price": "65000", "stock": "15"},
        {"id": "2", "name": "Laptop HP 15-inch", "price": "120000", "stock": "8"},
        {"id": "3", "name": "Casque JBL", "price": "12000", "stock": "50"}
    ]
    
    bulk_insert_products(r, products)
    print("Bulk insert avec pipeline terminé.")
    
    r.hset("cart:user:42", "1", 1)
    print("Panier avant checkout:", r.hgetall("cart:user:42"))
    checkout_cart(r, "user:42")
    print("Panier après checkout:", r.hgetall("cart:user:42"))
