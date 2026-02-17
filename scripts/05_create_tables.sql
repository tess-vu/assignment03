-- Part 5: Create BigQuery external tables with hive partitioning
--
-- Create new external tables that use the hive-partitioned folder
-- structure from 05_upload_to_gcs. BigQuery can automatically detect
-- the partition key (airnow_date) from folder names like:
--     airnow_date=2024-07-01/data.csv
--
-- This allows BigQuery to prune partitions when filtering by date,
-- so queries like WHERE airnow_date = '2024-07-15' only scan one
-- day's file instead of all 31.


-- Hourly Observations — CSV (hive-partitioned)
-- TODO: Create external table `hourly_observations_csv_hive`
-- pointing to gs://<your-bucket>/air_quality/hourly/csv/*
-- with hive partitioning options


-- Hourly Observations — JSON-L (hive-partitioned)
-- TODO: Create external table `hourly_observations_jsonl_hive`
-- pointing to gs://<your-bucket>/air_quality/hourly/jsonl/*
-- with hive partitioning options


-- Hourly Observations — Parquet (hive-partitioned)
-- TODO: Create external table `hourly_observations_parquet_hive`
-- pointing to gs://<your-bucket>/air_quality/hourly/parquet/*
-- with hive partitioning options

