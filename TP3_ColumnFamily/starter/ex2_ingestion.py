"""
TP3 - Exercice 2 : Ingestion de données IoT
Use Case : SmartGrid DZ - 10 000 capteurs, 5 minutes de mesures
"""
from cassandra.cluster import Cluster
from cassandra.io.asyncioreactor import AsyncioConnection
from cassandra.query import BatchStatement, BatchType
import uuid
import random
from datetime import datetime, timedelta
import time

CASSANDRA_HOST = 'localhost'
KEYSPACE = 'smartgrid'
NB_CAPTEURS = 10000
MINUTES_HISTORIQUE = 5

WILAYAS = ["Alger", "Oran", "Constantine", "Annaba", "Blida"]
COMMUNES = {
    "Alger": ["Bab Ezzouar", "Hydra", "El Harrach", "Dar El Beida"],
    "Oran": ["Bir El Djir", "Es Senia", "Arzew"],
    "Constantine": ["El Khroub", "Ain Smara", "Hamma Bouziane"],
    "Annaba": ["El Bouni", "El Hadjar", "Seraidi"],
    "Blida": ["Bougara", "Boufarik", "Larbaa"],
}

def connect():
    """Connexion au cluster Cassandra avec support Python 3.12+"""
    cluster = Cluster([CASSANDRA_HOST], connection_class=AsyncioConnection)
    session = cluster.connect(KEYSPACE)
    return session, cluster

def generate_mesure(capteur_id, wilaya, commune, timestamp):
    tension_base = 220
    return {
        "capteur_id": capteur_id,
        "date_jour": timestamp.date(),
        "timestamp": timestamp,
        "wilaya": wilaya,
        "commune": commune,
        "tension_v": round(tension_base + random.gauss(0, 5), 2),
        "courant_a": round(random.uniform(0.5, 15.0), 2),
        "puissance_kw": round(random.uniform(0.1, 3.3), 3),
        "frequence_hz": round(50 + random.gauss(0, 0.1), 2),
        "temperature": round(random.uniform(20, 65), 1),
        "alerte": random.random() < 0.05,
        "code_alerte": "VOLT_WARN" if random.random() < 0.05 else None
    }

def run_ingestion(session):
    print(f"Démarrage ingestion : {NB_CAPTEURS} capteurs × {MINUTES_HISTORIQUE} min")
    start = time.time()
    
    capteurs = []
    for _ in range(NB_CAPTEURS):
        w = random.choice(WILAYAS)
        c = random.choice(COMMUNES[w])
        capteurs.append((uuid.uuid4(), w, c))
    
    insert_stmt = session.prepare('''
        INSERT INTO mesures_par_capteur (capteur_id, date_jour, timestamp, wilaya, commune, tension_v, courant_a, puissance_kw, frequence_hz, temperature, alerte, code_alerte)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''')

    alert_stmt = session.prepare('''
        INSERT INTO alertes_par_wilaya (wilaya, date_jour, timestamp, capteur_id, code_alerte, description, gravite, resolue)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''')

    now = datetime.now()
    batch = BatchStatement(batch_type=BatchType.UNLOGGED)
    
    total_inserted = 0
    
    for m in range(MINUTES_HISTORIQUE):
        current_time = now - timedelta(minutes=m)
        date_str = current_time.strftime('%Y-%m-%d')
        for i, (cid, w, c) in enumerate(capteurs):
            mesure = generate_mesure(cid, w, c, current_time)
            batch.add(insert_stmt, (mesure["capteur_id"], date_str, mesure["timestamp"], mesure["wilaya"], mesure["commune"], mesure["tension_v"], mesure["courant_a"], mesure["puissance_kw"], mesure["frequence_hz"], mesure["temperature"], mesure["alerte"], mesure["code_alerte"]))
            
            if mesure["alerte"]:
                batch.add(alert_stmt, (mesure["wilaya"], date_str, mesure["timestamp"], mesure["capteur_id"], mesure["code_alerte"] or "WARN", "Alerte générée", 2, False))
            
            if len(batch) >= 50:
                session.execute(batch)
                batch.clear()
                total_inserted += 50
    
    if len(batch) > 0:
        session.execute(batch)
        total_inserted += len(batch)

    elapsed = time.time() - start
    print(f"\\n✅ {total_inserted:,} opérations insérées en {elapsed:.1f}s")
    print(f"   Débit : {total_inserted/elapsed:,.0f} requêtes/seconde")

if __name__ == "__main__":
    session, cluster = connect()
    run_ingestion(session)
    cluster.shutdown()
