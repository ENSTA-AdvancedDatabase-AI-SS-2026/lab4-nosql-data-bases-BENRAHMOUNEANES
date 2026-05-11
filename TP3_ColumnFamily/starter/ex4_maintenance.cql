USE smartgrid;

-- 4.1 Choisir la stratégie de compaction pour chaque table
-- TWCS is best for time series data because it drops old data efficiently via TTLs and groups data by time windows.

-- 4.2 Configurer TWCS pour les mesures
ALTER TABLE mesures_par_capteur
WITH compaction = {
  'class': 'TimeWindowCompactionStrategy',
  'compaction_window_unit': 'DAYS',
  'compaction_window_size': 1
};

-- 4.3 Vérifier l'utilisation des TTL
-- You can't query expiration dates directly easily without selecting TTL(column) 
-- SELECT TTL(tension_v) FROM mesures_par_capteur LIMIT 10;

-- 4.4 Analyser une partition "hot"
-- Detect using nodetool tablestats or nodetool cfhistograms. Fix by splitting partition keys (e.g., adding month/day to the partition key).
