# src/clean_merge.py

import pandas as pd
import os
from src.utils.config_loader import load_config

def load_data(api_path: str, web_path: str):
    df_api = pd.read_csv(api_path)
    df_web = pd.read_csv(web_path)
    print(f"Loaded API data: {df_api.shape} rows")
    print(f"Loaded Web data: {df_web.shape} rows")
    return df_api, df_web

def clean_api_data(df_api: pd.DataFrame) -> pd.DataFrame:
    # Select relevant columns
    cols = [
        'name', 'date_utc', 'rocket', 'success', 'payloads', 'launchpad'
    ]
    df = df_api[cols].copy()

    # Convert types
    df['date'] = pd.to_datetime(df['date_utc'])
    df['success'] = df['success'].astype('Int64')  # Allows NaNs

    # Rename for consistency
    df = df.rename(columns={
        'name': 'Mission',
        'success': 'class',
        'launchpad': 'Launch Site',
    })

    return df

def clean_web_data(df_web: pd.DataFrame) -> pd.DataFrame:
    # Drop unnamed columns or footnotes if any
    df_web = df_web.loc[:, ~df_web.columns.str.contains('^Unnamed')]

    # Optional: remove rows where there is no booster info
    df_web = df_web[df_web['Booster version'].notna()]

    # Clean up column names
    df_web.columns = df_web.columns.str.strip().str.replace('\n', ' ').str.replace(r'\[.*?\]', '', regex=True)

    return df_web

def main():
    config = load_config()
    api_csv = os.path.join(config["output_dir"], config["api_output_file"])
    web_csv = os.path.join(config["output_dir"], config["web_output_file"])
    output_csv = os.path.join(config["output_dir"], config["launch_dash_file"])

    # Loading the two tables
    df_api, df_web = load_data(api_csv, web_csv)
    df_api_clean = clean_api_data(df_api)
    # columns:rocket,payloads,launchpad,cores,flight_number,date_utc,date,BoosterVersion,longitude,latitude,launch_site,
    ## payload_mass,orbit,block,reused_count,serial,outcome,flights,gridfins,reused,legs,landing_pad

    df_web_clean = clean_web_data(df_web)
    # columns:Flight No.,Launch site,Payload,Payload mass,Orbit,Customer,Launch outcome,Version Booster,Booster landing,Date,Time

    # Merging along ???
    ## We want a dataframe that contains these columns
    column_names = [
    'Flight Number', 
    'Date', 
    'Booster Version', 
    'Payload Mass (kg)', 
    'Orbit', 
    'Launch Site', 
    'Launch Outcome', 
    'class', 
    'Booster Version Category'
]
    # Create empty DataFrame
    df_merged = pd.DataFrame(columns=column_names)
#    df = pd.merge(df_api_clean, df_web_clean, how='left', on='Flight Number')

    # Save merged or selected clean DataFrame
    # (Here: saving cleaned API version for dashboard use)
    df_merged.to_csv(output_csv, index=False)
    print(f"Cleaned data saved to {output_csv}")

if __name__ == "__main__":
    main()
