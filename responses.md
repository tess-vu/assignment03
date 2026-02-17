# Assignment 03 Responses

## Part 4: BigQuery External Tables

### Hourly Observations — CSV External Table SQL

```sql
-- Paste your CREATE EXTERNAL TABLE statement here (use a wildcard URI)
```

### Hourly Observations — JSON-L External Table SQL

```sql
-- Paste your CREATE EXTERNAL TABLE statement here (use a wildcard URI)
```

### Hourly Observations — Parquet External Table SQL

```sql
-- Paste your CREATE EXTERNAL TABLE statement here (use a wildcard URI)
```

### Site Locations — CSV External Table SQL

```sql
-- Paste your CREATE EXTERNAL TABLE statement here
```

### Site Locations — JSON-L External Table SQL

```sql
-- Paste your CREATE EXTERNAL TABLE statement here
```

### Site Locations — GeoParquet External Table SQL

```sql
-- Paste your CREATE EXTERNAL TABLE statement here
```

### Cross-Table Join Query

```sql
-- Paste your query that joins hourly observations with site locations here
```

---

## Part 5: Hive-Partitioned External Tables

### Hourly Observations — CSV (hive-partitioned)

```sql
-- Paste your CREATE EXTERNAL TABLE statement with hive partitioning options
```

### Hourly Observations — JSON-L (hive-partitioned)

```sql
-- Paste your CREATE EXTERNAL TABLE statement with hive partitioning options
```

### Hourly Observations — Parquet (hive-partitioned)

```sql
-- Paste your CREATE EXTERNAL TABLE statement with hive partitioning options
```

---

## Part 6: Analysis & Reflection

### 1. File Sizes

**Hourly data (single day):**

| Format  | File Size |
|---------|-----------|
| CSV     |           |
| JSON-L  |           |
| Parquet |           |

**Site locations:**

| Format     | File Size |
|------------|-----------|
| CSV        |           |
| JSON-L     |           |
| GeoParquet |           |

**Analysis:**
> [Your answer here — which is smallest/largest and why?]

### 2. Format Anatomy

> [Pick two formats and describe their structure. What are the key differences?]

### 3. Choosing Formats for BigQuery

> [Why is Parquet preferred over CSV or JSON-L? Consider performance and cost.]

### 4. Pipeline vs. Warehouse Joins

> [You kept hourly data and site locations as separate tables and joined them in BigQuery. What if you had joined them during the prepare step instead (denormalization)? What are the trade-offs of each approach?]

#### Stretch Challenge (optional)

If you implemented the stretch challenge (scripts `06_prepare`, `06_upload_to_gcs`, `06_create_tables.sql`), paste your SQL statements here:

```sql
-- Merged Hourly + Sites — CSV (hive-partitioned)
```

```sql
-- Merged Hourly + Sites — JSON-L (hive-partitioned)
```

```sql
-- Merged Hourly + Sites — GeoParquet (hive-partitioned)
```

### 5. Choosing a Data Source

For each person below, which air quality data source (AirNow hourly files, AirNow API, AQS bulk downloads, or AQS API) would you recommend, and why?

**a) A parent who wants a dashboard showing current air quality near their child's school:**
> [Your answer here]

**b) An environmental justice advocate identifying neighborhoods with chronically poor air quality over the past decade:**
> [Your answer here]

**c) A school administrator who needs automated morning alerts when AQI exceeds a threshold:**
> [Your answer here]
