# Assignment 03 Responses

## Part 4: BigQuery External Tables

### Hourly Observations — CSV External Table SQL

```sql
create or replace external table air_quality.hourly_observations_csv
options (
    format = 'CSV',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/*.csv'
    ],
    skip_leading_rows = 1
);
```

### Hourly Observations — JSON-L External Table SQL

```sql
create or replace external table air_quality.hourly_observations_jsonl
options (
    format = 'JSON',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/*.jsonl'
    ]
);
```

### Hourly Observations — Parquet External Table SQL

```sql
create or replace external table air_quality.hourly_observations_parquet
options (
    format = 'PARQUET',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/*.parquet'
    ]
);
```

### Site Locations — CSV External Table SQL

```sql
create or replace external table air_quality.site_locations_csv
options (
    format = 'CSV',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/sites/site_locations.csv'
    ],
    skip_leading_rows = 1
);
```

### Site Locations — JSON-L External Table SQL

```sql
create or replace external table air_quality.site_locations_jsonl
options (
    format = 'JSON',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/sites/site_locations.jsonl'
    ]
);
```

### Site Locations — GeoParquet External Table SQL

```sql
create or replace external table air_quality.site_locations_geoparquet
options (
    format = 'PARQUET',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/sites/site_locations.geoparquet'
    ]
);
```

### Cross-Table Join Query

```sql
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
```

---

## Part 5: Hive-Partitioned External Tables

### Hourly Observations — CSV (hive-partitioned)

```sql
create or replace external table air_quality.hourly_observations_csv_hive
with partition columns (
    airnow_date date
)
options (
    format = 'CSV',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/csv/*'
    ],
    hive_partition_uri_prefix
    = 'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/csv/',
    skip_leading_rows = 1
);
```

### Hourly Observations — JSON-L (hive-partitioned)

```sql
create or replace external table air_quality.hourly_observations_jsonl_hive
with partition columns (
    airnow_date date
)
options (
    format = 'JSON',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/jsonl/*'
    ],
    hive_partition_uri_prefix
    = 'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/jsonl/'
);
```

### Hourly Observations — Parquet (hive-partitioned)

```sql
create or replace external table air_quality.hourly_observations_parquet_hive
with partition columns (
    airnow_date date
)
options (
    format = 'PARQUET',
    uris = [
        'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/parquet/*'
    ],
    hive_partition_uri_prefix
    = 'gs://musa5090-s26-tvu-data-lake/air_quality/hourly/parquet/'
);
```

---

## Part 6: Analysis & Reflection

### 1. File Sizes

**Hourly data (single day 07-04-2024):**

| Format  | File Size |
|---------|-----------|
| CSV     | 18.7 MB   |
| JSON-L  | 44.4 MB   |
| Parquet | 812.1 KB  |

**Site locations:**

| Format     | File Size |
|------------|-----------|
| CSV        | 1 MB      |
| JSON-L     | 2.9 MB    |
| GeoParquet | 486.4 KB  |

**Analysis:**
> Which is smallest/largest and why?

The smallest is the Geo/Parquet file, which is known to be one of the fastest file types to read as opposed to the JSON-L file, which is the largest file. This difference is attributed to how they are stored, because the reason why Parquet is so much smaller is because it's constructed in machine-readable binary and is columnar versus the JSON-L's human-readable row-based plain text format.

### 2. Format Anatomy

> Pick two formats and describe their structure. What are the key differences?

CSV:

```
valid_date,valid_time,aqsid,site_name,gmt_offset,parameter_name,reporting_units,value,data_source
07/04/24,00:00,000010601,Goose Bay,-4.0,OZONE,PPB,27.0,Canadian Air and Precipitation Monitoring Network
```

JSON-L:

```
{"valid_date":"07\/04\/24","valid_time":"00:00","aqsid":"000010601","site_name":"Goose Bay","gmt_offset":-4.0,"parameter_name":"OZONE","reporting_units":"PPB","value":27.0,"data_source":"Canadian Air and Precipitation Monitoring Network"}
```

Both the CSV and JSON-L formats are human-readable formats with CSV having headers at the very top that denote what the corresponding values below are whereas JSON-L provides them in key-value pairs in a dictionary, so essentially the headers at the top seen in CSVs are seen in each JSON-L line alongside their associated value.

### 3. Choosing Formats for BigQuery

> Why is Parquet preferred over CSV or JSON-L? Consider performance and cost.

Parquet is preferred for big data because it's so much smaller compared to CSV and JSON-L, significantly reducing storage and costs for cloud computing. Because it's columnar in its structure, it can be column pruned where it reads only the columns needed and can skip the rest, making the search efficient. Its counterparts in this assignment need to be read from the start throughout the entire file until it hits the target. Behind this row-based versus columnar structure is the mechanism of the size differences, the fact that the columns are all of the same type makes Parquet much easier to commpress. Parquet is also preferred due to its enforced schema that defines the column names and their data types inside the file, in addition, the user can add new columns to the dataset without rewriting old files, which would have `null` values for new columns in old data.

### 4. Pipeline vs. Warehouse Joins

> You kept hourly data and site locations as separate tables and joined them in BigQuery. What if you had joined them during the prepare step instead (denormalization)? What are the trade-offs of each approach?

Between normalized and denormalized structures in databasing, the former splits the unnormalized data into smaller piecewise, related tables. This means that there's no redundancy, it's easier to update, and it's more efficient to store due to the fact that multiple subjects don't show up more than once because they are associated with a different class' subject. However, a denormalized structure creates a single table that has all the related tables joined, in this case the hourly and site location datasets, even if some of the data that a user may be looking for isn't needed. If I were to join in the prepare step and denormalize it, this simplifies the querying significantly and I wouldn't have to join the normalized tables in BigQuery and deal with a longer run-time for SQL queries. Realistically, it would be best to use a combination of these methods depending on use-case.

#### Stretch Challenge (optional)

If you implemented the stretch challenge (scripts `06_prepare`, `06_upload_to_gcs`, `06_create_tables.sql`), paste your SQL statements here:

```sql
-- Merged Hourly + Sites — CSV (hive-partitioned)
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
```

```sql
-- Merged Hourly + Sites — JSON-L (hive-partitioned)
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
```

```sql
-- Merged Hourly + Sites — GeoParquet (hive-partitioned)
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
```

### 5. Choosing a Data Source

For each person below, which air quality data source (AirNow hourly files, AirNow API, AQS bulk downloads, or AQS API) would you recommend, and why?

**a) A parent who wants a dashboard showing current air quality near their child's school:**
> I'd recommend the AirNow API since it's in real-time and can be used to create apps or dashboards as the parent wants current air quality around a specific location.

**b) An environmental justice advocate identifying neighborhoods with chronically poor air quality over the past decade:**
> I'd recommend the bulk downloads for AQS data due to the data being QA'd in addition to the fact that it's a historical archive of air quality for environmental justice research and advocacy.

**c) A school administrator who needs automated morning alerts when AQI exceeds a threshold:**
> I'd recommend the AirNow API as it allows for real-time air quality measurements and allows automated queries to provide the user any alerts when the AQI exceeds a specific threshold. It also provides any forecasting data in case alerts need to be based on that as opposed to hourly updates as well.
