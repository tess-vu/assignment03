"""
    Script to extract AirNow data files for a range of dates.

    This script downloads hourly air quality observation data and monitoring
    site location data from the EPA's AirNow program. Files are saved into
    a date-organized folder structure under data/raw/.

    AirNow files are hosted at:
        https://files.airnowtech.org/?prefix=airnow/

    Usage:
        python scripts/01_extract.py
"""

import pathlib
import requests

DATA_DIR = pathlib.Path(__file__).parent.parent / 'data'


def download_data_for_date(date_str):
    """Download AirNow data files for a single date.

    Downloads all 24 HourlyData files (hours 00-23) and the
    Monitoring_Site_Locations_V2.dat file for the specified date,
    saving them into data/raw/YYYY-MM-DD/.

    Args:
        date_str: Date string in 'YYYY-MM-DD' format. For example, '2024-07-01'.
    """
    # Make directory for the dates.
    (DATA_DIR / f"raw/{date_str}").mkdir(parents = True, exist_ok = True)

    # Construct the URL prefix for the given date.
    url_prefix = f"https://files.airnowtech.org/airnow/2024/{date_str.replace('-', '')}/"
    print(f"  {date_str}/")

    # Download HourlyData files for hours 00-23.
    try:
        for hour in range(24):
            hourly_url = f"{url_prefix}HourlyData_{date_str.replace('-', '')}{hour:02d}.dat"

            response = requests.get(hourly_url, timeout = 5)

            if response.status_code == 200:
                with open(DATA_DIR / f"raw/{date_str}/HourlyData_{date_str.replace('-', '')}{hour:02d}.dat", "wb") as f:
                    f.write(response.content)
                    print(f"    HourlyData_{date_str.replace('-', '')}{hour:02d}.dat")
            else:
                print(f"Failed: {hourly_url}")
    except requests.ConnectTimeout as e:
        print(f"Request didn't connect with the target server.\n{e}")
    except requests.Timeout as e:
        print(f"Maximum time exceeded for establishing a connection.\n{e}")

    # Download Monitoring_Site_Locations_V2.dat
    try:
        site_locations_url = f"{url_prefix}Monitoring_Site_Locations_V2.dat"
        
        response = requests.get(site_locations_url, timeout = 5)

        if response.status_code == 200:
            with open(DATA_DIR / f"raw/{date_str}/Monitoring_Site_Locations_V2.dat", "wb") as f:
                f.write(response.content)
                print(f"    Monitoring_Site_Locations_V2.dat")
        else:
            print(f"Failed: {site_locations_url}")
    except requests.ConnectTimeout as e:
        print(f"Request didn't connect with the target server.\n{e}")
    except requests.Timeout as e:
        print(f"Maximum time exceeded for establishing a connection.\n{e}")


if __name__ == "__main__":
    import datetime

    # Download data for July 2024
    start_date = datetime.date(2024, 7, 1)
    end_date = datetime.date(2024, 7, 31)

    current_date = start_date

    print("data/raw/")

    while current_date <= end_date:
        #print(f'Downloading data for {current_date}...')
        download_data_for_date(current_date.isoformat())
        current_date += datetime.timedelta(days = 1)

    print("Done.")
