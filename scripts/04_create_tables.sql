-- Part 4: Create BigQuery external tables
--
-- Create these tables in a dataset named `air_quality`.
-- Use wildcard URIs for the hourly data tables so a single table
-- spans all 31 days of files.
--
-- After creating the tables, verify they work by running:
--     SELECT count(*) FROM air_quality.<table_name>;
create schema if not exists air_quality;

-- Hourly Observations — CSV
-- TODO: Create external table `hourly_observations_csv`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.csv
create or replace external table air_quality.hourly_observations_csv
options (
    format = 'CSV',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/*.csv'
    ],
    skip_leading_rows = 1
);

-- Hourly Observations — JSON-L
-- TODO: Create external table `hourly_observations_jsonl`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.jsonl
create or replace external table air_quality.hourly_observations_jsonl
options (
    format = 'JSON',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/*.jsonl'
    ]
);

-- Hourly Observations — Parquet
-- TODO: Create external table `hourly_observations_parquet`
-- pointing to gs://<your-bucket>/air_quality/hourly/*.parquet
create or replace external table air_quality.hourly_observations_parquet
options (
    format = 'PARQUET',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/*.parquet'
    ]
);

-- Site Locations — CSV
-- TODO: Create external table `site_locations_csv`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.csv
create or replace external table air_quality.site_locations_csv
options (
    format = 'CSV',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/sites/site_locations.csv'
    ],
    skip_leading_rows = 1
);

-- Site Locations — JSON-L
-- TODO: Create external table `site_locations_jsonl`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.jsonl
create or replace external table air_quality.site_locations_jsonl
options (
    format = 'JSON',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/sites/site_locations.jsonl'
    ]
);

-- Site Locations — GeoParquet
-- TODO: Create external table `site_locations_geoparquet`
-- pointing to gs://<your-bucket>/air_quality/sites/site_locations.geoparquet
create or replace external table air_quality.site_locations_geoparquet
options (
    format = 'PARQUET',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/sites/site_locations.geoparquet'
    ]
);

-- Verify counts of hourly observation data.
select count(*) from air_quality.hourly_observations_csv;
select count(*) from air_quality.hourly_observations_jsonl;
select count(*) from air_quality.hourly_observations_parquet;

-- Cross-table join query
-- Write a query that joins hourly observations with site locations
-- to get latitude/longitude for each observation. For example,
-- find the average PM2.5 value by state for a single day.
select
-- Select StateAbbreviation and create avg_pm25 using average of value.
    sites.`StateAbbreviation`,
    avg(obs.value) as avg_pm25
-- Join hourly observations with site locations on shared AQSID.
from air_quality.hourly_observations_parquet as obs
inner join air_quality.site_locations_geoparquet as sites
    on obs.aqsid = sites.`AQSID`
-- Filter for PM2.5 air pollutant for date 07/04.
where
    obs.parameter_name = 'PM2.5'
    and obs.valid_date = '07/04/24'
-- Group by the state abbreviation and order by highest to lowest.
group by sites.`StateAbbreviation`
order by avg_pm25 desc;
