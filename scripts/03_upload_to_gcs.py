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


DATA_DIR = pathlib.Path(__file__).parent.parent / 'data'

# TODO: Update this to your bucket name
BUCKET_NAME = 'musa5090-s26-yourname-data'


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
    raise NotImplementedError("Implement this function to upload files to GCS.")


if __name__ == '__main__':
    upload_prepared_data()
    print('Done.')
