USE powergrid;

-- TWCS config for sensors
ALTER TABLE sensor_data
WITH compaction = {
  'class': 'TimeWindowCompactionStrategy',
  'compaction_window_unit': 'DAYS',
  'compaction_window_size': 1
};
