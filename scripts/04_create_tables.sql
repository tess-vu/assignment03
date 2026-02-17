-- Part 4: Create BigQuery external tables
--
-- Create these tables in a dataset named `air_quality`.
-- Use wildcard URIs for the hourly data tables so a single table
-- spans all 31 days of files.
--
-- After creating the tables, verify they work by running:
--     SELECT count(*) FROM air_quality.<table_name>;


-- Hourly Observations — CSV
-- TODO: Create external table `hourly_observations_csv`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.csv


-- Hourly Observations — JSON-L
-- TODO: Create external table `hourly_observations_jsonl`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.jsonl


-- Hourly Observations — Parquet
-- TODO: Create external table `hourly_observations_parquet`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.parquet


-- Site Locations — CSV
-- TODO: Create external table `site_locations_csv`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.csv


-- Site Locations — JSON-L
-- TODO: Create external table `site_locations_jsonl`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.jsonl


-- Site Locations — GeoParquet
-- TODO: Create external table `site_locations_geoparquet`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.geoparquet


-- Cross-table join query
-- Write a query that joins hourly observations with site locations
-- to get latitude/longitude for each observation. For example,
-- find the average PM2.5 value by state for a single day.

