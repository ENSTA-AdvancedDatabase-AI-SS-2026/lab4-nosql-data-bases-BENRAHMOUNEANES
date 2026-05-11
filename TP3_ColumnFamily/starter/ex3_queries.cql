USE smartgrid;

-- 3.1 Mesures d'un capteur spécifique sur les dernières 6 heures
-- SELECT * FROM mesures_par_capteur WHERE capteur_id = 123e4567-e89b-12d3-a456-426614174000 AND date_jour = '2023-10-01' AND timestamp >= '2023-10-01 10:00:00';

-- 3.2 Dernière mesure de chaque capteur d'une wilaya
-- Cassandra cannot group by and select latest easily without a different table or ALLOW FILTERING,
-- but for a specific capteur we can do LIMIT 1
-- SELECT * FROM mesures_par_capteur WHERE capteur_id = 123e4567-e89b-12d3-a456-426614174000 AND date_jour = '2023-10-01' LIMIT 1;

-- 3.3 Capteurs en alerte dans la wilaya "Alger" aujourd'hui
-- SELECT COUNT(*) FROM alertes_par_wilaya WHERE wilaya = 'Alger' AND date_jour = '2023-10-01';
-- SELECT * FROM alertes_par_wilaya WHERE wilaya = 'Alger' AND date_jour = '2023-10-01';

-- 3.4 Consommation totale par heure sur une journée (dashboard)
-- SELECT wilaya, date_heure, puissance_moy_kw FROM agregats_horaires WHERE wilaya = 'Alger' AND date_heure >= '2023-10-01 00:00:00' AND date_heure <= '2023-10-01 23:59:59';

-- 3.5 Détection d'anomalie : capteurs avec tension < 200V ou > 240V dans les 30 dernières minutes
-- We need a specific table for this, or query the alertes_par_wilaya table.
-- SELECT * FROM alertes_par_wilaya WHERE wilaya = 'Alger' AND date_jour = '2023-10-01' AND timestamp >= '2023-10-01 10:30:00';

-- 3.6 Top 10 capteurs les plus actifs
-- Cassandra is not suited for top 10 queries without an explicit table or analytics tool (like Spark).

-- 3.7 Requête ALLOW FILTERING : Pourquoi éviter ?
-- It forces scanning the entire table/partition, which is a massive performance hit.
-- Better to create a new table where the query columns are partition keys.
