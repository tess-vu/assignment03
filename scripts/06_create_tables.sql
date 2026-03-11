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
create or replace external table air_quality.hourly_with_sites_csv
with partition columns (
    airnow_date date
)
options (
    format = 'CSV',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly_with_sites/csv/*'
    ],
    hive_partition_uri_prefix
    = 'gs://musa5090-s26-tvu-data-lake/air_quality/hourly_with_sites/csv/',
    skip_leading_rows = 1
);

-- Merged Hourly + Sites — JSON-L (hive-partitioned)
-- TODO: Create external table `hourly_with_sites_jsonl`
-- pointing to gs://<your-bucket>/air_quality/hourly_with_sites/jsonl/*
-- with hive partitioning options
create or replace external table air_quality.hourly_with_sites_jsonl
with partition columns (
    airnow_date date
)
options (
    format = 'JSON',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly_with_sites/jsonl/*'
    ],
    hive_partition_uri_prefix
    = 'gs://musa5090-s26-tvu-data-lake/air_quality/hourly_with_sites/jsonl/'
);

-- Merged Hourly + Sites — GeoParquet (hive-partitioned)
-- TODO: Create external table `hourly_with_sites_geoparquet`
-- pointing to gs://<your-bucket>/air_quality/hourly_with_sites/geoparquet/*
-- with hive partitioning options
create or replace external table air_quality.hourly_with_sites_geoparquet
with partition columns (
    airnow_date date
)
options (
    format = 'PARQUET',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly_with_sites/geoparquet/*'
    ],
    hive_partition_uri_prefix
    = 'gs://musa5090-s26-tvu-data-lake/air_quality/hourly_with_sites/geoparquet/'
);

-- Check partition column.
select distinct airnow_date
from air_quality.hourly_with_sites_geoparquet
order by airnow_date;

-- Test partition pruning.
select count(*)
from air_quality.hourly_with_sites_geoparquet
where airnow_date = '2024-07-04';
