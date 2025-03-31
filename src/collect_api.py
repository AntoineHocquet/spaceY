# src/collect_api.py

import requests
import pandas as pd
import os
from src.utils.config_loader import load_config


def fetch_spacex_launch_data(api_url: str) -> pd.DataFrame:
    """
    Fetch SpaceX launch data from API and return as a DataFrame.
    Returns: pandas dataframe, containing at least the 6 columns:
     'name', 'date_utc', 'rocket', 'success', 'payloads', 'launchpad'
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
    # loads configuration file to get api url and csv path
    config = load_config()
    api_url = config["spacex_api_url"]
    output_path = os.path.join(config["output_dir"], config["api_output_file"])
    
    df = fetch_spacex_launch_data(api_url)
    save_to_csv(df, output_path)

if __name__ == "__main__":
    main()
