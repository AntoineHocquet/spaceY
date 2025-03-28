# src/collect_api.py

import requests
import pandas as pd
import os

def fetch_spacex_launch_data(api_url: str) -> pd.DataFrame:
    """
    Fetch SpaceX launch data from API and return as a DataFrame.
    """
    print(f"Fetching data from {api_url}")
    response = requests.get(api_url)
    response.raise_for_status()
    launches = response.json()
    df = pd.json_normalize(launches)
    print(f"Retrieved {len(df)} launches.")
    return df

def save_to_csv(df: pd.DataFrame, output_path: str):
    """
    Save DataFrame to CSV.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved data to {output_path}")

def main():
    api_url = "https://api.spacexdata.com/v4/launches"
    output_csv = "data/spacex_api_data.csv"
    
    df = fetch_spacex_launch_data(api_url)
    save_to_csv(df, output_csv)

if __name__ == "__main__":
    main()
