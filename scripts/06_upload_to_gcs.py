"""
Stretch challenge: Upload merged hourly + site location data to GCS.

This script uploads the denormalized (merged) files produced by
06_prepare.py to GCS with a hive-partitioned folder structure.

Prerequisites:
    - Run `gcloud auth application-default login` to authenticate.
    - Part 6 prepare script (06_prepare.py) should be complete.

Usage:
    python scripts/06_upload_to_gcs.py
"""

import pathlib


DATA_DIR = pathlib.Path(__file__).parent.parent / "data"

# TODO: Update this to your bucket name
BUCKET_NAME = "musa5090-s26-yourname-data"


def upload_merged_data():
    """Upload merged hourly data to GCS with hive-partitioned folder structure.

    Expected GCS structure:
        gs://<bucket>/air_quality/hourly_with_sites/csv/airnow_date=2024-07-01/data.csv
        gs://<bucket>/air_quality/hourly_with_sites/jsonl/airnow_date=2024-07-01/data.jsonl
        gs://<bucket>/air_quality/hourly_with_sites/geoparquet/airnow_date=2024-07-01/data.geoparquet
    """
    raise NotImplementedError("Implement this function to upload merged data to GCS.")


if __name__ == "__main__":
    upload_merged_data()
    print("Done.")
