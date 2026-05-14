"""
TP1 - Exercice 2 : Sessions utilisateur
Use Case : ShopFast - Gestion des sessions avec TTL
"""
import redis
import uuid

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create_session(r, user_id, ttl=1800):
    sid = str(uuid.uuid4())
    r.set(f"sess:{sid}", user_id, ex=ttl)
    return sid

def get_session_user(r, sid):
    k = f"sess:{sid}"
    uid = r.get(k)
    if uid:
        r.expire(k, 1800)
    return uid

def kill_session(r, sid):
    r.delete(f"sess:{sid}")

if __name__ == "__main__":
    r.flushdb()
    token = create_session(r, "anes_b")
    print(f"Token: {token}")
    print(f"User: {get_session_user(r, token)}")
    kill_session(r, token)
