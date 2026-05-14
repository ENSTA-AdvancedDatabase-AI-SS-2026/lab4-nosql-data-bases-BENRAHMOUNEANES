CREATE KEYSPACE IF NOT EXISTS powergrid
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};

USE powergrid;

CREATE TABLE IF NOT EXISTS sensor_data (
  sid UUID,
  day DATE,
  ts TIMESTAMP,
  city TEXT,
  v_val FLOAT,
  a_val FLOAT,
  kw_val FLOAT,
  is_alert BOOLEAN,
  PRIMARY KEY ((sid, day), ts)
) WITH CLUSTERING ORDER BY (ts DESC);

CREATE TABLE IF NOT EXISTS regional_alerts (
  region TEXT,
  day DATE,
  ts TIMESTAMP,
  sid UUID,
  msg TEXT,
  level INT,
  PRIMARY KEY ((region, day), ts, sid)
) WITH CLUSTERING ORDER BY (ts DESC);

CREATE TABLE IF NOT EXISTS hourly_stats (
  region TEXT,
  hr TIMESTAMP,
  avg_kw FLOAT,
  max_kw FLOAT,
  alert_count COUNTER,
  PRIMARY KEY ((region), hr)
) WITH CLUSTERING ORDER BY (hr DESC);
