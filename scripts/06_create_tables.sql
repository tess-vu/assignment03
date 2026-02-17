-- Part 6 (stretch challenge): Create BigQuery external tables for merged data
--
-- These tables point to the denormalized files where hourly observations
-- have been pre-joined with site location data during the prepare step.
-- Each observation row already includes latitude, longitude, state, etc.
--
-- Use hive partitioning with the airnow_date partition key.


-- Merged Hourly + Sites — CSV (hive-partitioned)
-- TODO: Create external table `hourly_with_sites_csv`
-- pointing to gs://<your-bucket>/air_quality/hourly_with_sites/csv/*
-- with hive partitioning options


-- Merged Hourly + Sites — JSON-L (hive-partitioned)
-- TODO: Create external table `hourly_with_sites_jsonl`
-- pointing to gs://<your-bucket>/air_quality/hourly_with_sites/jsonl/*
-- with hive partitioning options


-- Merged Hourly + Sites — GeoParquet (hive-partitioned)
-- TODO: Create external table `hourly_with_sites_geoparquet`
-- pointing to gs://<your-bucket>/air_quality/hourly_with_sites/geoparquet/*
-- with hive partitioning options

