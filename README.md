# Assignment 03

**Complete by March 5, 2026**

## Motivation

Air quality data powers a wide range of **recurring, real-world decisions** — from a parent checking whether it's safe for their child to play outside, to a public health official deciding whether to issue an air quality advisory, to an urban planner evaluating a proposed zoning change near an industrial corridor. These aren't one-time research questions; they're operational decisions that people make again and again, where having current data changes the action they take. (See [MOTIVATION.md](MOTIVATION.md) for detailed examples and a discussion of how to choose the right data source for different use cases.)

Tools like [AirNow](https://www.airnow.gov/) and [Windy](https://www.windy.com/) serve these decisions — but behind every data product like these is a **data pipeline** that takes raw source data and prepares it for querying, mapping, and action. In this assignment, you'll work with EPA's AirNow hourly monitoring data to practice the **Extract** and **Load** portions of an EtLT pipeline, with separate steps for downloading, transforming, and uploading data.

## Learning Objectives

- Understand what "the cloud" is and why it matters for data products
- Work with multiple file formats (including non-CSV formats) and understand their trade-offs
- Parse, combine, and join datasets programmatically
- Write scripts (Python or JavaScript) that download, convert, and upload data
- Create a cloud storage bucket and upload files to it programmatically
- Create BigQuery external tables — including tables backed by multiple files
- Understand hive partitioning and when to join data in a pipeline vs. at query time

## Instructions

1.  Fork this repository to your own account.
2.  Clone your fork to your local machine.
3.  Complete the parts below.
4.  Push your changes to your fork.
5.  Submit a pull request to the original repository. Your pull request should have your name in the title (e.g. `Assignment 03 - Mjumbe Poe`).

## Dataset

We will use two datasets published by the EPA's [AirNow](https://www.airnow.gov/) program, both available as file downloads from [files.airnowtech.org](https://files.airnowtech.org/?prefix=airnow/):

### 1. Hourly Observation Data

Files named `HourlyData_YYYYMMDDHH.dat`, containing one hour of air quality observations from monitoring sites across the US and Canada. Organized by date in folders like `airnow/YYYY/YYYYMMDD/`.

- **Format:** Pipe-delimited (`|`), no header row
- **Columns:** `valid_date | valid_time | aqsid | site_name | gmt_offset | parameter_name | reporting_units | value | data_source`
- **Size:** ~700KB per file, ~7,300 rows per hour
- **Example URL:** `https://s3-us-west-1.amazonaws.com/files.airnowtech.org/airnow/2024/20240701/HourlyData_2024070112.dat`
- **Documentation:** [HourlyDataFactSheet.pdf](https://docs.airnowapi.org/docs/HourlyDataFactSheet.pdf)

### 2. Monitoring Site Locations (Version 2)

A file named `Monitoring_Site_Locations_V2.dat` containing geographic coordinates and metadata for each monitoring site. We're using the **version 2** format, which is less well-documented in older tutorials but is a strict superset of version 1 — it adds fields like `FullAQSID` (12-digit ID with country code), `MonitorType` (Permanent/Temporary), and uses modern CBSA naming. Adapting older material should be straightforward.

- **Format:** Pipe-delimited (`|`), with a header row
- **Key columns include:** `StationID`, `AQSID`, `FullAQSID`, `Parameter`, `MonitorType`, `SiteName`, `Latitude`, `Longitude`, `CountryFIPS`, `StateAbbreviation`, `CountyName`, and more
- **Example URL:** `https://s3-us-west-1.amazonaws.com/files.airnowtech.org/airnow/2024/20240701/Monitoring_Site_Locations_V2.dat`
- **Documentation:** [MonitoringSiteV2FactSheet.pdf](https://docs.airnowapi.org/docs/MonitoringSiteV2FactSheet.pdf)

> **Important:** The site locations file has **one row per site-parameter combination** — so a site that monitors both O₃ and PM2.5 will have two rows. You'll need to deduplicate by site when you prepare this data (see Part 2).

> **Note on data size:** A month of hourly data is ~720 files totaling roughly **500MB**. Make sure you're downloading to a location with sufficient disk space. The `data/` folder is gitignored, so these files won't be pushed to your repository.

---

## Part 1: Extract (Download Raw Data)

A starter script has been provided for you in `scripts/01_extract.py` (or `scripts/01_extract.mjs` if you prefer JavaScript). It contains a function stub that accepts a date string and should download all the AirNow data files for that date.

**Your task:** Implement the function so that it:

1.  **Downloads** all 24 `HourlyData` files (hours 00–23) for the given date from `files.airnowtech.org`.
2.  **Downloads** the `Monitoring_Site_Locations_V2.dat` file for that date.
3.  **Saves** all files into a date-organized folder structure under `data/raw/`.

Then call the function in a loop to download data for **every day in July 2024** (2024-07-01 through 2024-07-31).

> **Why a full month?** This extraction step takes real time — roughly 10–15 minutes. That's intentional. One of the reasons we separate extraction from transformation is that we don't want to re-download hundreds of megabytes every time we need to re-process the data. Once the raw files are on disk, you can re-run your transform step as many times as you need without hitting the network again.

**Expected output structure:**
```
data/raw/
  2024-07-01/
    HourlyData_2024070100.dat
    HourlyData_2024070101.dat
    ...
    HourlyData_2024070123.dat
    Monitoring_Site_Locations_V2.dat
  2024-07-02/
    ...
  2024-07-31/
    ...
```

**Deliverables:**
-   Your completed script in `scripts/01_extract.py` (or `scripts/01_extract.mjs`)

---

## Part 2: Transform (Prepare for Loading)

A starter script has been provided in `scripts/02_prepare.py` (or `scripts/02_prepare.mjs`). It contains function stubs for converting the raw `.dat` files into formats that BigQuery can use as external table sources.

**Your task:** Implement the functions to convert the data into the following formats:

### Hourly observation data → CSV, JSON-L, and Parquet

For each date, combine the 24 raw hourly `.dat` files into a single output file per format. You'll need to assign column names since the raw files have no header row.

### Site locations → CSV, JSON-L, and GeoParquet

Convert the monitoring site locations file into each format. Since the site locations file includes latitude and longitude, the GeoParquet output should include a **geometry column** with point geometries.

> **Important:** Remember that the raw site locations file has one row per site-parameter combination. When preparing the site locations data, **deduplicate so there is one row per site** (e.g., keep the first occurrence of each `AQSID`). This will make joins cleaner later.

Then run your transform for **every day in July 2024** — processing the data you already downloaded in Part 1. This is the simplest form of a **backfill**: you're going back over previously-extracted data and preparing it in the formats you need.

**Expected output structure:**
```
data/prepared/
  hourly/
    2024-07-01.csv
    2024-07-01.jsonl
    2024-07-01.parquet
    2024-07-02.csv
    ...
  sites/
    site_locations.csv
    site_locations.jsonl
    site_locations.geoparquet
```

> **Note:** You may use any libraries you prefer. Some useful ones:
> - **Python:** `pandas`, `geopandas`, `shapely`, `pyarrow`
> - **JavaScript:** `@turf/helpers`, `csv-parse`, `parquet-wasm`

**Deliverables:**
-   Your completed script in `scripts/02_prepare.py` (or `scripts/02_prepare.mjs`)
-   The converted files should go in `data/prepared/` (gitignored — I will run your scripts to generate them)

---

## Part 3: Upload to Cloud Storage (GCS)

A starter script has been provided in `scripts/03_upload_to_gcs.py` (or `scripts/03_upload_to_gcs.mjs`).

**Your task:** Implement the script to:

1.  Authenticate with Google Cloud using your local credentials (via `gcloud auth application-default login`).
2.  Upload the prepared files from Part 2 to a GCS bucket in your project.
    - Name the bucket something unique like `musa5090-s26-<yourname>-data`.
    - Preserve the folder structure so that hourly files are under `air_quality/hourly/` and site files are under `air_quality/sites/`.

> _You can create the bucket manually in the GCP Console or programmatically in your script — either is fine._

**Deliverables:**
-   Your completed script in `scripts/03_upload_to_gcs.py` (or `scripts/03_upload_to_gcs.mjs`)

---

## Part 4: BigQuery External Tables

A starter SQL file has been provided in `scripts/04_create_tables.sql`.

Using the BigQuery console:

1.  Create a dataset named `air_quality`.
2.  Create **external tables** linked to the files you uploaded. Use **wildcard URIs** (e.g., `gs://your-bucket/air_quality/hourly/*.csv`) for the hourly data so that a single table spans all 31 days of files:

    **Hourly observations:**
    -   `hourly_observations_csv` (wildcard over `hourly/*.csv`)
    -   `hourly_observations_jsonl` (wildcard over `hourly/*.jsonl`)
    -   `hourly_observations_parquet` (wildcard over `hourly/*.parquet`)

    **Site locations:**
    -   `site_locations_csv` (pointing to `sites/site_locations.csv`)
    -   `site_locations_jsonl` (pointing to `sites/site_locations.jsonl`)
    -   `site_locations_geoparquet` (pointing to `sites/site_locations.geoparquet`)

3.  Run a `SELECT count(*) FROM ...` query on each hourly table to verify they have the same row count.

4.  **Cross-table join:** Write a query that joins the hourly observations with the site locations to get the **latitude and longitude** for each observation. For example, find the average PM2.5 value by state for a single day.

**Deliverables:**
-   Save your `CREATE EXTERNAL TABLE` SQL statements and cross-table join query in `scripts/04_create_tables.sql`.
-   Also paste them into `responses.md`.

---

## Part 5: Hive Partitioning

In Part 3, you uploaded the hourly files with names like `2024-07-01.csv`. This works, but BigQuery can't tell _which_ dates are in _which_ files without scanning all of them. **Hive partitioning** solves this by encoding metadata in the folder structure.

A starter script has been provided in `scripts/05_upload_to_gcs.py` (or `scripts/05_upload_to_gcs.mjs`), along with a SQL file `scripts/05_create_tables.sql`.

**Your task:**

1.  Implement the upload script to **re-upload** your prepared hourly files to GCS with a hive-partitioned folder structure. Instead of:
    ```
    air_quality/hourly/2024-07-01.csv
    ```
    Upload as:
    ```
    air_quality/hourly/csv/airnow_date=2024-07-01/data.csv
    air_quality/hourly/jsonl/airnow_date=2024-07-01/data.jsonl
    air_quality/hourly/parquet/airnow_date=2024-07-01/data.parquet
    ```

2.  Create new external tables with **hive partitioning options** so that BigQuery automatically recognizes `airnow_date` as a partition column. This means queries like `WHERE airnow_date = '2024-07-15'` only scan one day's file instead of all 31.

> **This is a backfill of the upload step.** You don't need to re-download or re-transform anything — you're re-uploading the same files from `data/prepared/` with a different folder structure. This is exactly the kind of situation where separating your pipeline steps pays off.

**Deliverables:**
-   Your completed script in `scripts/05_upload_to_gcs.py` (or `scripts/05_upload_to_gcs.mjs`)
-   Save your hive-partitioned `CREATE EXTERNAL TABLE` SQL in `scripts/05_create_tables.sql`
-   Also paste them into `responses.md`

---

## Part 6: Analysis & Reflection

Edit [`responses.md`](responses.md) to answer the following questions:

1.  **File Sizes:** List the file size for each format you generated (for a single day's hourly data, and for the site locations). Which is the smallest? Which is the largest? Why do you think that is?
2.  **Format Anatomy:** Pick any two of the formats you worked with (e.g., CSV vs. Parquet, or JSON-L vs. GeoParquet). Describe the general structure/anatomy of each and what makes them different.
3.  **Choosing Formats for BigQuery:** Why is Parquet generally preferred over CSV or JSON-L for use with BigQuery external tables? Think about both _performance_ and _cost_.
4.  **Pipeline vs. Warehouse Joins:** In this assignment, you kept the hourly observations and site locations as separate tables and joined them in BigQuery at query time. An alternative approach would be to join them during the Prepare step and produce a single denormalized file with coordinates included in every observation row. What are the trade-offs of each approach? When might you prefer one over the other?

    > **Stretch challenge:** Implement the alternative! Use the starter scripts `scripts/06_prepare.py` (or `.mjs`), `scripts/06_upload_to_gcs.py` (or `.mjs`), and `scripts/06_create_tables.sql` to:
    > - Write a new prepare script that joins hourly data with site locations during transformation
    > - Upload the merged files with hive partitioning
    > - Create external tables for the merged data
    >
    > This is another backfill — you're re-processing the same raw data with a different transformation, without re-downloading anything.

5.  **Choosing a Data Source:** Read the [MOTIVATION.md](MOTIVATION.md) document. For each of the following people, which air quality data source (AirNow hourly files, AirNow API, AQS bulk downloads, or AQS API) would you recommend they use to build their data product, and why?
    1.  A parent who wants a dashboard showing current air quality near their child's school
    2.  An environmental justice advocate identifying neighborhoods with chronically poor air quality over the past decade
    3.  A school administrator who needs automated morning alerts when AQI exceeds a threshold
