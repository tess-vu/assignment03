"""
Script to upload prepared data files to Google Cloud Storage (GCS).

This script uploads the transformed files from data/prepared/ to a
GCS bucket, preserving the folder structure so that BigQuery can
use wildcard URIs to create external tables across multiple files.

Prerequisites:
    - Run `gcloud auth application-default login` to authenticate.
    - Create a GCS bucket (manually or in this script).

Usage:
    python scripts/03_upload_to_gcs.py
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

BUCKET_NAME = os.getenv("DATA_LAKE_BUCKET")


def upload_prepared_data():
    """Upload all prepared data files to GCS.

    Uploads the contents of data/prepared/ to the GCS bucket,
    preserving the folder structure under a prefix of 'air_quality/'.

    Expected GCS structure:
        gs://<bucket>/air_quality/hourly/2024-07-01.csv
        gs://<bucket>/air_quality/hourly/2024-07-01.jsonl
        gs://<bucket>/air_quality/hourly/2024-07-01.parquet
        ...
        gs://<bucket>/air_quality/sites/site_locations.csv
        gs://<bucket>/air_quality/sites/site_locations.jsonl
        gs://<bucket>/air_quality/sites/site_locations.geoparquet
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
    upload_prepared_data()
    print("Done.")
