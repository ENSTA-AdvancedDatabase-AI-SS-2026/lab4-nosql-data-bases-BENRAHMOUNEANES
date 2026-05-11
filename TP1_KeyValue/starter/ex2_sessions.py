"""
TP1 - Exercice 2 : Sessions utilisateur
Use Case : ShopFast - Gestion des sessions avec TTL
"""
import redis
import uuid

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def create_session(r, user_id: str) -> str:
    """Créer une session avec TTL de 30 minutes (1800s)"""
    session_id = str(uuid.uuid4())
    session_key = f"session:{session_id}"
    r.set(session_key, user_id, ex=1800)
    return session_id

def get_session(r, session_id: str) -> str:
    """Récupérer la session et renouveler le TTL (sliding expiration)"""
    session_key = f"session:{session_id}"
    user_id = r.get(session_key)
    if user_id:
        r.expire(session_key, 1800)
    return user_id

def delete_session(r, session_id: str):
    """Supprimer la session"""
    session_key = f"session:{session_id}"
    r.delete(session_key)

if __name__ == "__main__":
    r.flushdb()
    sid = create_session(r, "user:42")
    print(f"Created session: {sid} for user:42")
    print(f"Get session: {get_session(r, sid)}")
    delete_session(r, sid)
    print(f"After deletion: {get_session(r, sid)}")
