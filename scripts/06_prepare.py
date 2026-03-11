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
import pandas as pd
import geopandas as gpd

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

def prepare_merged_csv(date_str):
    """Merge hourly observations with site locations and write as CSV.

    Reads the hourly .dat files for the given date and the site locations
    file, joins them on AQSID, and writes to
    data/prepared/hourly_with_sites/<date>.csv.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    try:
        # Create output directory.
        (DATA_DIR / "prepared/hourly_with_sites").mkdir(parents=True, exist_ok=True)
        output_dir = "prepared/hourly_with_sites"

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
            hourly = pd.read_csv(
                filename, sep="|", header=None, names=HOURLY_COLUMNS, encoding="latin-1"
            )

            # Append DataFrame to list.
            combined_list.append(hourly)

        # Combine all DataFrames.
        combined_df = pd.concat(combined_list)

        # Find most recent site locations file.
        raw_folders = [f for f in (DATA_DIR / "raw").iterdir() if f.is_dir()]
        most_recent = sorted(raw_folders)[-1]
        sites_path = most_recent / "Monitoring_Site_Locations_V2.dat"

        # Read site locations.
        sites_df = pd.read_csv(sites_path, sep="|")

        # Deduplicate by AQSID.
        sites_df = sites_df.drop_duplicates(subset=["AQSID"])

        # Merge hourly data with site locations.
        merged_df = pd.merge(
            combined_df, 
            sites_df, 
            left_on="aqsid", 
            right_on="AQSID", 
            how="left"
        )

        # Write combined DataFrame to CSV.
        merged_df.to_csv(DATA_DIR / output_dir / f"{date_str}.csv", index=False)
        print(f"    {date_str}.csv")

    except FileNotFoundError as e:
        print(f"File not found.\n{e}")
    except pd.errors.EmptyDataError as e:
        print(f"No data in file.\n{e}")
    except PermissionError as e:
        print(f"User doesn't have permissions.\n{e}")


def prepare_merged_jsonl(date_str):
    """Merge hourly observations with site locations and write as JSON-L.

    Reads the hourly .dat files for the given date and the site locations
    file, joins them on AQSID, and writes to
    data/prepared/hourly_with_sites/<date>.jsonl.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    try:
        # Create output directory.
        (DATA_DIR / "prepared/hourly_with_sites").mkdir(parents=True, exist_ok=True)
        output_dir = "prepared/hourly_with_sites"

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
            hourly = pd.read_csv(
                filename, sep="|", header=None, names=HOURLY_COLUMNS, encoding="latin-1"
            )

            # Append DataFrame to list.
            combined_list.append(hourly)

        # Combine all DataFrames.
        combined_df = pd.concat(combined_list)

        # Find most recent site locations file.
        raw_folders = [f for f in (DATA_DIR / "raw").iterdir() if f.is_dir()]
        most_recent = sorted(raw_folders)[-1]
        sites_path = most_recent / "Monitoring_Site_Locations_V2.dat"

        # Read site locations.
        sites_df = pd.read_csv(sites_path, sep="|")

        # Deduplicate by AQSID.
        sites_df = sites_df.drop_duplicates(subset=["AQSID"])

        # Merge hourly data with site locations.
        merged_df = pd.merge(
            combined_df, 
            sites_df, 
            left_on="aqsid", 
            right_on="AQSID", 
            how="left"
        )

        # Write combined DataFrame to json.
        merged_df.to_json(DATA_DIR / output_dir / f"{date_str}.jsonl", orient="records", lines=True)
        print(f"    {date_str}.jsonl")

    except FileNotFoundError as e:
        print(f"File not found.\n{e}")
    except pd.errors.EmptyDataError as e:
        print(f"No data in file.\n{e}")
    except PermissionError as e:
        print(f"User doesn't have permissions.\n{e}")


def prepare_merged_geoparquet(date_str):
    """Merge hourly observations with site locations and write as GeoParquet.

    Reads the hourly .dat files for the given date and the site locations
    file, joins them on AQSID, creates point geometries from the site's
    latitude and longitude, and writes to
    data/prepared/hourly_with_sites/<date>.geoparquet.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format.
    """
    try:
        # Create output directory.
        (DATA_DIR / "prepared/hourly_with_sites").mkdir(parents=True, exist_ok=True)
        output_dir = "prepared/hourly_with_sites"

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
            hourly = pd.read_csv(
                filename, sep="|", header=None, names=HOURLY_COLUMNS, encoding="latin-1"
            )

            # Append DataFrame to list.
            combined_list.append(hourly)

        # Combine all DataFrames.
        combined_df = pd.concat(combined_list)

        # Find most recent site locations file.
        raw_folders = [f for f in (DATA_DIR / "raw").iterdir() if f.is_dir()]
        most_recent = sorted(raw_folders)[-1]
        sites_path = most_recent / "Monitoring_Site_Locations_V2.dat"

        # Read site locations.
        sites_df = pd.read_csv(sites_path, sep="|")

        # Deduplicate by AQSID.
        sites_df = sites_df.drop_duplicates(subset=["AQSID"])

        # Merge hourly data with site locations.
        merged_df = pd.merge(
            combined_df, 
            sites_df, 
            left_on="aqsid", 
            right_on="AQSID", 
            how="left"
        )

        # Create geometry from site coordinates.
        geometry = gpd.points_from_xy(merged_df["Longitude"], merged_df["Latitude"])

        # Convert to GeoDataFrame.
        merged_gdf = gpd.GeoDataFrame(merged_df, geometry=geometry, crs="EPSG:4326")

        # Write combined DataFrame to geoparquet.
        merged_gdf.to_parquet(DATA_DIR / output_dir / f"{date_str}.geoparquet", index=False)
        print(f"    {date_str}.geoparquet")

    except FileNotFoundError as e:
        print(f"File not found.\n{e}")
    except pd.errors.EmptyDataError as e:
        print(f"No data in file.\n{e}")
    except PermissionError as e:
        print(f"User doesn't have permissions.\n{e}")


if __name__ == "__main__":
    import datetime

    print("data/prepared/")
    print("  hourly_with_sites/")

    # Backfill: prepare merged data for each day in July 2024
    start_date = datetime.date(2024, 7, 1)
    end_date = datetime.date(2024, 7, 31)

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.isoformat()
        prepare_merged_csv(date_str)
        prepare_merged_jsonl(date_str)
        prepare_merged_geoparquet(date_str)
        current_date += datetime.timedelta(days=1)

    print("Done.")
