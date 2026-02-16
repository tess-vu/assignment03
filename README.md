# Assignment 03

**Complete by March 5, 2026**

## Motivation

Air quality data powers a wide range of **recurring, real-world decisions** — from a parent checking whether it's safe for their child to play outside, to a public health official deciding whether to issue an air quality advisory, to an urban planner evaluating a proposed zoning change near an industrial corridor. These aren't one-time research questions; they're operational decisions that people make again and again, where having current data changes the action they take. (See [MOTIVATION.md](MOTIVATION.md) for detailed examples.)

Tools like [AirNow](https://www.airnow.gov/) and [Windy](https://www.windy.com/) serve these decisions — but behind every data product like these is a **data pipeline** that takes raw source data and prepares it for querying, mapping, and action. The EPA publishes air quality monitoring data as bulk CSV files. To make it useful, someone has to extract those files, convert them into efficient formats, load them into cloud storage, and make them queryable in a data warehouse. That's the **Extract** and **Load** portions of an EtLT pipeline — and that's what you'll practice in this assignment.

## Learning Objectives

- Understand what "the cloud" is and why it matters for data products
- Work with multiple geospatial file formats and understand their trade-offs
- Write scripts (Python or JavaScript) that download, convert, and upload data
- Create a cloud storage bucket and upload files to it programmatically
- Create BigQuery external tables that point to files in cloud storage

## Instructions

1.  Fork this repository to your own account.
2.  Clone your fork to your local machine.
3.  Complete the parts below.
4.  Push your changes to your fork.
5.  Submit a pull request to the original repository. Your pull request should have your name in the title (e.g. `Assignment 03 - Mjumbe Poe`).

## Dataset

We will use the **EPA Air Quality System (AQS)** daily summary data for **PM2.5** (fine particulate matter) for **2024**.

- **Download page:** [EPA AQS Pre-Generated Data Files](https://aqs.epa.gov/aqsweb/airdata/download_files.html)
- **Direct link:** [`daily_88101_2024.zip`](https://aqs.epa.gov/aqsweb/airdata/daily_88101_2024.zip)
- **File format documentation:** [AirData File Formats](https://aqs.epa.gov/aqsweb/airdata/FileFormats.html)

The file is a CSV inside a zip archive. Each row represents one daily summary for one monitor. The data includes columns for `Latitude` and `Longitude` (the monitor's location), `AQI` (Air Quality Index), `Arithmetic Mean`, `State Name`, `County Name`, and more. There are roughly **500K–1M+ rows** in a single year of data.

> **Why PM2.5?** Fine particulate matter is one of the most important air pollutants for public health and environmental justice research. It's linked to respiratory illness, cardiovascular disease, and premature death, and its levels vary significantly by neighborhood and proximity to pollution sources.

---

## Part 1: Data Extraction & Format Conversion

Write a script (in Python or JavaScript) that does the following:

1.  **Downloads** the PM2.5 daily summary zip file from the EPA URL above.
2.  **Unzips** the file and reads the CSV data inside.
3.  **Converts** the data into the following formats and saves them in the `data/` folder:
    *   **GeoJSON** (`.geojson`) — with point geometry created from the `Latitude` and `Longitude` columns
    *   **Newline-delimited JSON** (`.jsonl`) — one JSON object per line, with geometry embedded as a GeoJSON geometry object
    *   **CSV** (`.csv`) — the original format; keep the `Latitude` and `Longitude` columns as-is
    *   **GeoParquet** (`.parquet`) — with geometry column
    *   _(Bonus)_ **Shapefile** (`.shp` + sidecar files) — note the 10-character field name limit!

> **Note:** You may use any libraries you prefer. Some useful ones:
> - **Python:** `requests`, `geopandas`, `shapely`, `pandas`, `pyarrow`
> - **JavaScript:** `node-fetch`, `@turf/helpers`, `csv-parse`, `parquet-wasm`, `adm-zip`

**Deliverables:**
-   Your script in `scripts/extract_and_load.py` (or `scripts/extract_and_load.mjs`)
-   The converted files should go in `data/` (which is gitignored — I will run your script to generate them)

---

## Part 2: Upload to Cloud Storage (GCS)

Write a script (or extend the script from Part 1) that:

1.  Authenticates with Google Cloud using your local credentials (via `gcloud auth application-default login`).
2.  Uploads the converted files from Part 1 to a GCS bucket in your project.
    - Name the bucket something unique like `musa5090-s26-<yourname>-data`.
    - Create a folder (prefix) called `air_quality/` in the bucket.

> _You can create the bucket manually in the GCP Console or programmatically in your script — either is fine._

**Deliverables:**
-   The upload logic should be in `scripts/upload_to_gcs.py` (or `scripts/upload_to_gcs.mjs`)

---

## Part 3: BigQuery External Tables

Using the BigQuery console or SQL commands:

1.  Create a dataset named `air_quality`.
2.  Create **external tables** linked to the files you uploaded:
    -   `daily_aqi_csv` (pointing to your CSV file in GCS)
    -   `daily_aqi_jsonl` (pointing to your JSON-L file in GCS)
    -   `daily_aqi_parquet` (pointing to your Parquet file in GCS)
3.  Run a `SELECT count(*) FROM ...` query on each table to verify they work and that the row counts match.

**Deliverables:**
-   Paste your `CREATE EXTERNAL TABLE` SQL statements into `responses.md`.

---

## Part 4: Analysis & Reflection

Edit [`responses.md`](responses.md) to answer the following questions:

1.  **File Sizes:** List the file size for each format you generated. Which is the smallest? Which is the largest? Why do you think that is?
2.  **Format Anatomy:** Pick any two of the formats you worked with (e.g., GeoJSON vs. CSV, or Parquet vs. JSON-L). Describe the general structure/anatomy of each and what makes them different.
3.  **Choosing Formats for BigQuery:** Why is Parquet generally preferred over CSV or JSON-L for use with BigQuery external tables? Think about both _performance_ and _cost_.
4.  **Geometry Handling:** The original EPA data comes as a plain CSV with `Latitude` and `Longitude` columns. Describe how you embedded geometry information in at least two of the other formats you created. What decisions did you have to make?
