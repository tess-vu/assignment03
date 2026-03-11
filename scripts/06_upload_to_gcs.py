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


def upload_merged_data():
    """Upload merged hourly data to GCS with hive-partitioned folder structure.

    Expected GCS structure:
        gs://<bucket>/air_quality/hourly_with_sites/csv/airnow_date=2024-07-01/data.csv
        gs://<bucket>/air_quality/hourly_with_sites/jsonl/airnow_date=2024-07-01/data.jsonl
        gs://<bucket>/air_quality/hourly_with_sites/geoparquet/airnow_date=2024-07-01/data.geoparquet
    """
    try:
        # Create storage client.
        storage_client = storage.Client()

        # Get bucket reference.
        bucket = storage_client.bucket(BUCKET_NAME)

        # Define prepared directory path.
        hourly_dir = DATA_DIR / "prepared" / "hourly_with_sites"

        # Loop through all files recursively.
        for filepath in hourly_dir.rglob("*"):
            # Skip if not a file.
            if not filepath.is_file():
                continue

            # Get date portion "YYYY-MM-DD".
            date_str = filepath.stem

            # Get ".csv" suffix.
            extension = filepath.suffix

            # Remove dot for "csv".
            format_folder = extension[1:]

            # Construct hive-partitioned GCS path.
            gcs_path = f"air_quality/hourly_with_sites/{format_folder}/airnow_date={date_str}/data{extension}"

            # Create blob and upload.
            blob = bucket.blob(gcs_path)
            blob.upload_from_filename(str(filepath), timeout=600)

            # Print progress.
            print(f"Uploading: {gcs_path}")

    except gcs_exceptions.NotFound as e:
        print(f"Bucket does not exist.\n{e}")
    except auth_exceptions.DefaultCredentialsError as e:
        print(f"Authentication failed. Check credentials.\n{e}")
    except api_exceptions.GoogleAPIError as e:
        print(f"Network error.\n{e}")


if __name__ == "__main__":
    upload_merged_data()
    print("Done.")
