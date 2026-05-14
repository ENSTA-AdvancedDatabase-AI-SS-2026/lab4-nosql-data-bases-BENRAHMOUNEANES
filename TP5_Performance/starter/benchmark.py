import time
import redis
from pymongo import MongoClient
from cassandra.cluster import Cluster

def run_redis_bench(n=5000):
    r = redis.Redis(host='localhost', port=6379)
    t0 = time.time()
    with r.pipeline() as p:
        for i in range(n):
            p.set(f"b:{i}", "v")
            if i % 500 == 0: p.execute()
        p.execute()
    print(f"Redis: {n/(time.time()-t0):.1f} ops/s")

def run_mongo_bench(n=5000):
    c = MongoClient("mongodb://admin:admin123@localhost:27017/")
    col = c["bench_db"]["data"]
    col.delete_many({})
    docs = [{"_id": i, "v": "v"} for i in range(n)]
    t0 = time.time()
    col.insert_many(docs)
    print(f"Mongo: {n/(time.time()-t0):.1f} ops/s")

def run_cass_bench(n=5000):
    cl = Cluster(['localhost'])
    sess = cl.connect()
    sess.execute("CREATE KEYSPACE IF NOT EXISTS b_ks WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}")
    sess.execute("CREATE TABLE IF NOT EXISTS b_ks.t (id int PRIMARY KEY, v text)")
    stmt = sess.prepare("INSERT INTO b_ks.t (id, v) VALUES (?, 'v')")
    t0 = time.time()
    for i in range(n): sess.execute_async(stmt, [i])
    print(f"Cassandra: {n/(time.time()-t0):.1f} ops/s")

if __name__ == "__main__":
    print("NoSQL Performance Test")
    N = 2000
    run_redis_bench(N)
    run_mongo_bench(N)
    run_cass_bench(N)
rk terminé !")
