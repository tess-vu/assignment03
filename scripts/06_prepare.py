"""
Stretch challenge: Prepare merged hourly + site location data.

This script joins the hourly observation data with site location data
during the prepare step (denormalization), producing files where
each observation row includes the site's latitude, longitude, and
other geographic metadata.

This is the alternative to the approach in Part 4, where hourly data
and site locations were kept as separate tables and joined at query
time in BigQuery.

This is a backfill of the prepare step — you're re-processing the
same raw data you already downloaded, but with a different
transformation that produces a richer output.

Usage:
    python scripts/06_prepare.py
"""

import pathlib


DATA_DIR = pathlib.Path(__file__).parent.parent / "data"


def prepare_merged_csv(date_str):
    """Merge hourly observations with site locations and write as CSV.

    Reads the hourly .dat files for the given date and the site locations
    file, joins them on AQSID, and writes to
    data/prepared/hourly_with_sites/<date>.csv.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raise NotImplementedError("Implement this function.")


def prepare_merged_jsonl(date_str):
    """Merge hourly observations with site locations and write as JSON-L.

    Reads the hourly .dat files for the given date and the site locations
    file, joins them on AQSID, and writes to
    data/prepared/hourly_with_sites/<date>.jsonl.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raise NotImplementedError("Implement this function.")


def prepare_merged_geoparquet(date_str):
    """Merge hourly observations with site locations and write as GeoParquet.

    Reads the hourly .dat files for the given date and the site locations
    file, joins them on AQSID, creates point geometries from the site's
    latitude and longitude, and writes to
    data/prepared/hourly_with_sites/<date>.geoparquet.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    raise NotImplementedError("Implement this function.")


if __name__ == "__main__":
    import datetime

    # Backfill: prepare merged data for each day in July 2024
    start_date = datetime.date(2024, 7, 1)
    end_date = datetime.date(2024, 7, 31)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.isoformat()
        print(f"Preparing merged data for {date_str}...")
        prepare_merged_csv(date_str)
        prepare_merged_jsonl(date_str)
        prepare_merged_geoparquet(date_str)
        current_date += datetime.timedelta(days=1)

    print("Done.")
