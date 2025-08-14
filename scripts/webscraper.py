# ==============================================================================
# SCRIPT FOR ACADEMIC THESIS: WUNDERGROUND DAILY WEATHER DATA SCRAPER
#
# PURPOSE:
# This script is designed to systematically collect historical daily weather
# observation data for a specified location and date range. It was developed
# for thesis research requiring detailed meteorological time-series data.
#
# DATA SOURCE:
# This script downloads data directly from the official Weather Underground (WU)
# historical observations API. This approach was chosen for its high reliability,
# speed, and direct access to high-granularity, research-grade data, bypassing
# the need for browser automation or web scraping.
#
# METHODOLOGY:
# This script constructs a unique URL for each day in the specified range to
# query the WU API. It uses the 'requests' library to download the JSON data,
# then uses 'pandas' to parse this data directly into a DataFrame. The data
# for each day is collected and compiled into a single, final CSV file.
# ==============================================================================

import requests
import pandas as pd
from datetime import date, timedelta, datetime
import time
import os
import random


def get_weather_data(start_date_str, end_date_str, station_id, output_csv):
    """
    Downloads daily weather observation data from the official Weather Underground API.

    Args:
        start_date_str (str): The start date in 'YYYY-MM-DD' format.
        end_date_str (str): The end date in 'YYYY-MM-DD' format.
        station_id (str): The 4-letter ICAO station code (e.g., 'RCSS').
        output_csv (str): The name of the output CSV file.
    """
    print("Starting the data download process using the Official Wunderground API method...")

    # --- API Details ---
    # This is the official API endpoint for historical observations.
    base_url = f"https://api.weather.com/v1/location/{station_id}:9:TW/observations/historical.json"
    # This API key is publicly available in the website's source code.
    api_key = "e1f10a1e78da46f5b10a1e78da96f525"

    start_date = date.fromisoformat(start_date_str)
    end_date = date.fromisoformat(end_date_str)

    all_observations = []
    total_days = (end_date - start_date).days + 1

    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    # --- Loop Through Each Day ---
    current_date = start_date
    while current_date <= end_date:
        days_processed = (current_date - start_date).days
        date_for_api = current_date.strftime("%Y%m%d")

        # Define the parameters for the API request
        params = {
            'apiKey': api_key,
            'units': 'e',  # 'e' for Imperial units (Fahrenheit)
            'startDate': date_for_api,
            'endDate': date_for_api
        }

        print(f"Processing data for {date_for_api} ({days_processed + 1}/{total_days})...")

        try:
            # --- 1. Fetch the data ---
            response = session.get(base_url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()

            # --- 2. Process the JSON Response ---
            observations = data.get('observations', [])
            if not observations:
                print("  -> No observations found for this day.")
            else:
                for obs in observations:
                    # Convert Unix timestamp to the requested "YYYY-MM-DD HH:MM:SS" format
                    timestamp_str = "Invalid Timestamp"
                    try:
                        dt_object = datetime.fromtimestamp(obs.get('expire_time_gmt', 0))
                        timestamp_str = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                    except (ValueError, TypeError):
                        pass

                    row_data = {
                        'Timestamp': timestamp_str,
                        'Temperature': obs.get('temp'),
                        'Dew Point': obs.get('dewPt'),
                        'Humidity': obs.get('rh'),
                        'Wind': obs.get('wdir_cardinal'),
                        'Speed': obs.get('wspd'),
                        'Wind Gust': obs.get('gust'),
                        'Pressure': obs.get('pressure'),
                        'Precip.': obs.get('precip_hrly'),
                        'Condition': obs.get('wx_phrase')
                    }
                    all_observations.append(row_data)
                print(f"  -> Successfully downloaded {len(observations)} observations.")

        except requests.exceptions.RequestException as e:
            print(f"  -> An error occurred for {date_for_api}: {e}")
        except Exception as e:
            print(f"  -> An unexpected error occurred while processing {date_for_api}: {e}")

        current_date += timedelta(days=1)
        # Be respectful to the server
        time.sleep(random.uniform(1, 2))

    # --- 3. Create and Save DataFrame ---
    if not all_observations:
        print("\nNo data was downloaded. Exiting.")
        return

    print("\nDownload complete. Creating DataFrame and saving to CSV...")
    df = pd.DataFrame(all_observations)

    # Define and reorder final columns with the new Timestamp column
    final_headers = ["Timestamp", "Temperature", "Dew Point", "Humidity", "Wind", "Speed", "Wind Gust", "Pressure",
                     "Precip.", "Condition"]
    df = df[final_headers]

    try:
        df.to_csv(output_csv, index=False, encoding='utf-8')
        print(f"\nSuccess! Data has been saved to '{os.path.abspath(output_csv)}'")
    except Exception as e:
        print(f"\nError: Could not save the file. Reason: {e}")


if __name__ == '__main__':
    # --- Configuration ---
    START_DATE = "2024-05-03"
    END_DATE = "2025-06-22"
    STATION_ID = "RCSS"
    OUTPUT_FILE = "wunderground_weather.csv"

    # --- Run the Scraper ---
    get_weather_data(START_DATE, END_DATE, STATION_ID, OUTPUT_FILE)
