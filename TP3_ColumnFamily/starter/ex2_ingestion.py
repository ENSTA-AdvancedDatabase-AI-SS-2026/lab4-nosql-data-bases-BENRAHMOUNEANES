import uuid
import time
import random
from datetime import datetime, date, timedelta
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, BatchType

def push_iot_data(sess, count=100, span_min=5):
    print(f"Loading {count} sensors...")
    stmt = sess.prepare("INSERT INTO sensor_data (sid, day, ts, city, v_val, a_val, kw_val, is_alert) VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
    cities = ["Algiers", "Oran", "Setif", "Tlemcen"]
    
    t0 = time.time()
    for i in range(count):
        uid = uuid.uuid4()
        city = random.choice(cities)
        batch = BatchStatement(batch_type=BatchType.UNLOGGED)
        
        for m in range(span_min):
            now = datetime.now() - timedelta(minutes=m)
            batch.add(stmt, (uid, now.date(), now, city, 230.0 + random.uniform(-5, 5), 10.0, 2.3, False))
        
        sess.execute(batch)
    
    dt = time.time() - t0
    print(f"Done in {dt:.2f}s")

if __name__ == "__main__":
    cl = Cluster(['localhost'])
    s = cl.connect('powergrid')
    push_iot_data(s, 100, 5)
