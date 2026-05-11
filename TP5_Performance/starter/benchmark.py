"""
TP5 - Benchmark Comparatif NoSQL
Mesurer les performances de Redis, MongoDB, Cassandra, Neo4j
"""
import time
import statistics
import json
import threading
from typing import Callable, List, Tuple
import redis
from pymongo import MongoClient
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement, BatchType

def measure_latency(fn: Callable, iterations: int = 1000) -> dict:
    latencies = []
    for _ in range(iterations):
        start = time.perf_counter()
        fn()
        latencies.append((time.perf_counter() - start) * 1000)
    
    latencies.sort()
    return {
        "mean_ms": statistics.mean(latencies),
        "p50_ms": latencies[int(0.50 * len(latencies))],
        "p95_ms": latencies[int(0.95 * len(latencies))],
        "p99_ms": latencies[int(0.99 * len(latencies))],
        "max_ms": max(latencies),
        "throughput_rps": 1000 / statistics.mean(latencies) if statistics.mean(latencies) > 0 else 0
    }

def print_results(name: str, results: dict):
    print(f"\n{'='*50}")
    print(f" {name}")
    print(f"{'='*50}")
    for k, v in results.items():
        print(f"  {k:20s}: {v:.2f}")

def benchmark_write_redis(n: int = 100_000):
    r = redis.Redis(host='localhost', port=6379)
    r.flushdb()
    start = time.time()
    pipe = r.pipeline()
    for i in range(n):
        pipe.set(f"key:{i}", f"value:{i}")
        if i % 10000 == 0:
            pipe.execute()
    pipe.execute()
    elapsed = time.time() - start
    print(f"Redis Write {n} records: {elapsed:.2f}s, Throughput: {n/elapsed:.2f} rps")

def benchmark_write_mongodb(n: int = 100_000):
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    db = client["benchmark"]
    collection = db["test"]
    collection.delete_many({})
    
    start = time.time()
    batch = []
    for i in range(n):
        batch.append({"_id": i, "value": f"value:{i}"})
        if len(batch) >= 10000:
            collection.insert_many(batch)
            batch = []
    if batch:
        collection.insert_many(batch)
    elapsed = time.time() - start
    print(f"MongoDB Write {n} records: {elapsed:.2f}s, Throughput: {n/elapsed:.2f} rps")

def benchmark_write_cassandra(n: int = 100_000):
    cluster = Cluster(['localhost'])
    session = cluster.connect()
    session.execute("CREATE KEYSPACE IF NOT EXISTS benchmark WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};")
    session.execute("USE benchmark;")
    session.execute("CREATE TABLE IF NOT EXISTS test (id int PRIMARY KEY, value text);")
    session.execute("TRUNCATE test;")
    
    start = time.time()
    insert_stmt = session.prepare("INSERT INTO test (id, value) VALUES (?, ?)")
    batch = BatchStatement(batch_type=BatchType.UNLOGGED)
    
    total_inserted = 0
    for i in range(n):
        batch.add(insert_stmt, (i, f"value:{i}"))
        if len(batch) >= 50:
            session.execute(batch)
            batch.clear()
            total_inserted += 50
    if len(batch) > 0:
        session.execute(batch)
    elapsed = time.time() - start
    cluster.shutdown()
    print(f"Cassandra Write {n} records: {elapsed:.2f}s, Throughput: {n/elapsed:.2f} rps")

def benchmark_read_redis():
    r = redis.Redis(host='localhost', port=6379)
    def read_single():
        r.get("key:500")
    
    results = measure_latency(read_single, 1000)
    print_results("Redis Read Single", results)

def benchmark_read_mongodb():
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    collection = client["benchmark"]["test"]
    def read_single():
        collection.find_one({"_id": 500})
        
    results = measure_latency(read_single, 1000)
    print_results("MongoDB Read Single", results)

def benchmark_concurrent(db_fn: Callable, n_clients: int = 50, requests_per_client: int = 200):
    threads = []
    latencies = []
    
    def worker():
        for _ in range(requests_per_client):
            start = time.perf_counter()
            db_fn()
            latencies.append((time.perf_counter() - start) * 1000)

    for _ in range(n_clients):
        t = threading.Thread(target=worker)
        threads.append(t)
    
    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
        
    total_time = time.perf_counter() - start
    
    latencies.sort()
    results = {
        "mean_ms": statistics.mean(latencies),
        "p50_ms": latencies[int(0.50 * len(latencies))],
        "p95_ms": latencies[int(0.95 * len(latencies))],
        "p99_ms": latencies[int(0.99 * len(latencies))],
        "max_ms": max(latencies),
        "throughput_rps": (n_clients * requests_per_client) / total_time
    }
    print_results(f"Concurrent ({n_clients} clients)", results)

if __name__ == "__main__":
    print("🚀 Benchmark NoSQL - Comparatif des technologies")
    print("="*60)
    
    N = 10_000
    
    print(f"\\n📝 Benchmark Écriture ({N:,} enregistrements)")
    try:
        benchmark_write_redis(N)
    except Exception as e:
        print(f"Redis not available: {e}")
        
    try:
        benchmark_write_mongodb(N)
    except Exception as e:
        print(f"MongoDB not available: {e}")
        
    try:
        benchmark_write_cassandra(N)
    except Exception as e:
        print(f"Cassandra not available: {e}")
    
    print(f"\\n📖 Benchmark Lecture (1,000 requêtes)")
    try:
        benchmark_read_redis()
    except Exception as e:
        print(f"Redis not available: {e}")
        
    try:
        benchmark_read_mongodb()
    except Exception as e:
        print(f"MongoDB not available: {e}")
    
    print(f"\\n⚡ Test Charge Concurrente (50 clients)")
    try:
        r = redis.Redis(host='localhost', port=6379)
        benchmark_concurrent(lambda: r.get("key:10"), 50, 200)
    except Exception as e:
        print(f"Concurrent test not available: {e}")
    
    print("\\n✅ Benchmark terminé !")
