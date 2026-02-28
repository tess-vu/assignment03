"""
Script to transform raw AirNow data files into BigQuery-compatible formats.

This script reads the raw .dat files downloaded by 01_extract.py and converts
them into CSV, JSON-L, and Parquet formats suitable for loading into
BigQuery as external tables.

Hourly observation data is converted to: CSV, JSON-L, Parquet
Site location data is converted to: CSV, JSON-L, GeoParquet (with point geometry)

Usage:
    python scripts/02_prepare.py
"""

import pathlib
import pyarrow
import pandas as pd
import geopandas as gpd
import shapely

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"

HOURLY_COLUMNS = [
    "valid_date",
    "valid_time",
    "aqsid",
    "site_name",
    "gmt_offset",
    "parameter_name",
    "reporting_units",
    "value",
    "data_source",
]


# --- Hourly observation data ---


def prepare_hourly_csv(date_str):
    """Convert raw hourly .dat files for a date to a single CSV file.

    Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
    combines them into a single dataset, assigns column names,
    and writes to data/prepared/hourly/<date>.csv.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    try:
        # Create output directory.
        (DATA_DIR / f"prepared/hourly").mkdir(parents=True, exist_ok=True)
        output_dir = "prepared/hourly"

        # Empty list for DataFrames.
        combined_list = []

        # Loop through hours 00-23.
        for hour in range(24):
            # Build full path to hourly .dat file.
            filename = (
                DATA_DIR
                / f"raw/{date_str}/HourlyData_{date_str.replace('-', '')}{hour:02d}.dat"
            )

            # Read file into DataFrame.
            hourly = pd.read_csv(filename, sep="|", header=None, names=HOURLY_COLUMNS)

            # Append DataFrame to list.
            combined_list.append(hourly)

        # Combine all DataFrames.
        combined_df = pd.concat(combined_list)

        # Write combined DataFrame to CSV.
        combined_df.to_csv(DATA_DIR / output_dir / f"{date_str}.csv", index=False)
        print(f"    {date_str}.csv")

    except FileNotFoundError as e:
        print(f"File not found.\n{e}")
    except pd.errors.EmptyDataError as e:
        print(f"No data in file.\n{e}")
    except PermissionError as e:
        print(f"User doesn't have permissions.\n{e}")


def prepare_hourly_jsonl(date_str):
    """Convert raw hourly .dat files for a date to newline-delimited JSON.

    Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
    combines them, and writes one JSON object per line to
    data/prepared/hourly/<date>.jsonl.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raise NotImplementedError("Implement this function.")


def prepare_hourly_parquet(date_str):
    """Convert raw hourly .dat files for a date to Parquet format.

    Reads all 24 HourlyData_*.dat files from data/raw/<date>/,
    combines them, and writes to data/prepared/hourly/<date>.parquet.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raise NotImplementedError("Implement this function.")


# --- Site location data ---


def prepare_site_locations_csv():
    """Convert monitoring site locations to CSV.

    Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
    so there is one row per site (the raw file has one row per
    site-parameter combination), and writes to
    data/prepared/sites/site_locations.csv.

    Use the most recent date's file from data/raw/.
    """
    raise NotImplementedError("Implement this function.")


def prepare_site_locations_jsonl():
    """Convert monitoring site locations to newline-delimited JSON.

    Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
    so there is one row per site (the raw file has one row per
    site-parameter combination), and writes to
    data/prepared/sites/site_locations.jsonl.

    Use the most recent date's file from data/raw/.
    """
    raise NotImplementedError("Implement this function.")


def prepare_site_locations_geoparquet():
    """Convert monitoring site locations to GeoParquet with point geometry.

    Reads the Monitoring_Site_Locations_V2.dat file, deduplicates
    so there is one row per site (the raw file has one row per
    site-parameter combination), creates point geometries from
    latitude and longitude, and writes to
    data/prepared/sites/site_locations.geoparquet.

    Use the most recent date's file from data/raw/.
    """
    raise NotImplementedError("Implement this function.")


if __name__ == "__main__":
    import datetime

    # Prepare site locations (only need to do this once)
    print("Preparing site locations...")
    prepare_site_locations_csv()
    prepare_site_locations_jsonl()
    prepare_site_locations_geoparquet()

    # Prepare hourly data for each day in July 2024 (backfill)
    start_date = datetime.date(2024, 7, 1)
    end_date = datetime.date(2024, 7, 31)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.isoformat()

        print("data/prepared/")
        print("  hourly/")

        prepare_hourly_csv(date_str)

        prepare_hourly_jsonl(date_str)

        prepare_hourly_parquet(date_str)

        current_date += datetime.timedelta(days=1)

    print("Done.")
