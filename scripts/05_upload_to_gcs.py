"""
Script to re-upload prepared data to GCS using hive-partitioned folder structure.

This script takes the same prepared files from Part 2 and uploads them
to GCS with a hive-partitioned directory layout. Instead of flat files like:
    air_quality/hourly/2024-07-01.csv

Files are organized as:
    air_quality/hourly/csv/airnow_date=2024-07-01/data.csv

This enables BigQuery to automatically detect the partition key
(airnow_date) and use it for query pruning, so queries filtering
by date only scan the relevant files.

This is a backfill of the upload step — you don't need to re-download
or re-transform anything. You're just re-uploading the same files
with a different folder structure.

Prerequisites:
    - Run `gcloud auth application-default login` to authenticate.
    - Parts 1-3 should be complete (data already prepared and uploaded once).

Usage:
    python scripts/05_upload_to_gcs.py
"""

import pathlib
import os
from google.cloud import storage
from google.cloud import exceptions as gcs_exceptions
from google.auth import exceptions as auth_exceptions
from google.api_core import exceptions as api_exceptions
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = pathlib.Path(__file__).parent.parent / "data"

# TODO: Update this to your bucket name
BUCKET_NAME = os.getenv("DATA_LAKE_BUCKET")


def upload_with_hive_partitioning():
    """Upload prepared hourly data to GCS with hive-partitioned folder structure.

    For each date's prepared files, upload them to GCS with the following
    folder structure:
        gs://<bucket>/air_quality/hourly/csv/airnow_date=2024-07-01/data.csv
        gs://<bucket>/air_quality/hourly/jsonl/airnow_date=2024-07-01/data.jsonl
        gs://<bucket>/air_quality/hourly/parquet/airnow_date=2024-07-01/data.parquet

    The site locations files don't need hive partitioning (they're not
    date-partitioned), so you can re-upload them as-is or skip them.
    """
    try:
        # Create storage client.
        storage_client = storage.Client()

        # Get bucket reference.
        bucket = storage_client.bucket(BUCKET_NAME)

        # Define prepared directory path.
        prepared_dir = DATA_DIR / "prepared"

        # Loop through all files recursively.

        for filepath in prepared_dir.rglob("*"):
            # Skip if not a file.
            if not filepath.is_file():
                continue

            # Calculate relative path from prepared directory.
            relative_path = filepath.relative_to(prepared_dir).as_posix()

            # Construct GCS destination path with air_quality/ prefix.
            gcs_path = f"air_quality/{relative_path}"

            # Create blob and upload.
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(str(filepath))

            # Print progress.
            print(f"Uploading: {gcs_path}")

    except gcs_exceptions.NotFound as e:
        print(f"Bucket does not exist.\n{e}")
    except auth_exceptions.DefaultCredentialsError as e:
        print(f"Authentication failed. Check credentials.\n{e}")
    except api_exceptions.GoogleAPIError as e:
        print(f"Network error.\n{e}")


if __name__ == "__main__":
    upload_with_hive_partitioning()
    print("Done.")
