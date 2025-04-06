# src/clean_merge.py

import pandas as pd
import os
import re
from src.utils.config_loader import load_config

def load_data(api_path: str, web_path: str):
    df_api = pd.read_csv(api_path)
    df_web = pd.read_csv(web_path)
    print(f"Loaded API data: {df_api.shape} rows")
    print(f"Loaded Web data: {df_web.shape} rows")
    return df_api, df_web


def extract_date(date_series):
    return date_series.dt.date



def clean_api_data(df_api, remove_falcon_1=True):
    """"
    Input: pandas dataframe whose columns should be:
      rocket,payloads,launchpad,cores,flight_number,date_utc,date,BoosterVersion,
      longitude,latitude,launch_site,payload_mass,orbit,block,reused_count,serial,outcome,flights,
      gridfins,reused,legs,landing_pad
    Output: same dataframe but with corrected types and removed falcon 1 flights by default
    """
    # Convert types
    df_api['date'] = pd.to_datetime(df_api['date'])
    # df_api['outcome'] = df_api['outcome'].astype('Int64')  # Allows NaNs

    # Removes Falcon 1 boosters to keep only Falcon 9
    if remove_falcon_1:
        df_api=df_api[df_api['BoosterVersion']!='Falcon 1']
        print("Falcon 1 entries have been removed.")

    # Calculate the mean of PayloadMass column to replace the np.nan values
    mean_payload = df_api['payload_mass'].mean()
    df_api['payload_mass'].fillna(mean_payload, inplace=True)
    print("Missing Payload Mass entries have been replaced by mean value.")

    return df_api


def clean_Version_Booster(Version):
    """ cleans the 'Version Booster' column"""
    Version = Version.apply(lambda x: re.sub(r'[^\w\s\.]', '', str(x)))
    return Version


def clean_web_data(df_web, remove_falcon_1=True):
    """
    Args: pandas dataframe whose columns by default should be:
      Flight No.,Launch site,Payload,Payload mass,Orbit,Customer,
      Launch outcome,Version Booster,Booster landing,Date,Time
    Returns: Cleaner dataframe
    """
    # Drop unnamed columns or footnotes if any
    df_web = df_web.loc[:, ~df_web.columns.str.contains('^Unnamed')]

    # cleans the 'Version Booster' column
    df_web['Version Booster'] = clean_Version_Booster(df_web['Version Booster'])
    df_web['Version Booster'] = df_web['Version Booster'].str.strip()

    return df_web.copy()


def standardize_columns(df, column_map, lowercase=True):
    """
    Renames columns of a DataFrame based on a provided mapping.
    Args:
    - df (pd.DataFrame): The input DataFrame.
    - column_map (dict): Dictionary mapping current column names to standardized ones.
    - lowercase (bool): Whether to lowercase all column names after renaming.
    Returns:
    - pd.DataFrame: A copy of the DataFrame with standardized column names.
    """
    df = df.rename(columns=column_map)
    if lowercase:
        df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]
    return df.copy()


def create_class_attribute(df,verbose=False):
    """
    Uses the 'outcome' attribute to create a list where:
    - the element is zero if the corresponding row  in  'outcome' is in the set bad_outcome
    - the element is one otherwise.
    Then assigns it to the variable 'class'.
    Args: dataframe
    Returns: dataframe + new column 'class'
    """
    if verbose:
        print("\nThe landing outcomes are listed as follows:\n", df.outcome.value_counts())
    
    # define a set of bad outcomes (for which class is 0)
    bad_outcomes={'False ASDS', 'False Ocean', 'False RTLS', 'None ASDS', 'None None'}

    landing_class = []
    # loop to assign
    for landing_outcome in df.outcome:
        if landing_outcome in bad_outcomes:
            landing_class.append(0)
        else:
            landing_class.append(1)
    df['class']=landing_class

    return df



def main():
    config = load_config()
    api_csv = os.path.join(config["output_dir"], config["api_output_file"])
    web_csv = os.path.join(config["output_dir"], config["web_output_file"])
    output_csv = os.path.join(config["output_dir"], config["launch_dash_file"])

    # Loading the two tables
    df_api, df_web = load_data(api_csv, web_csv)

    # cleaning df_api & renaming columns
    df_api_clean = clean_api_data(df_api,remove_falcon_1=False)
    api_column_map = {
        'BoosterVersion': 'booster' # Falcon 1, Falcon 9 etc.
    }
    df_api_std = standardize_columns(df_api_clean, api_column_map)

    # cleaning df_web & renaming columns
    df_web_clean = clean_web_data(df_web)
    web_column_map = {
        'Flight No.': 'flight_number',
        'Launch site': 'launch_site',
        'Payload': 'payload',
        'Payload Mass (kg)': 'payload_mass',
        'Orbit': 'orbit',
        'Customer': 'customer',
        'Launch Outcome': 'launch_outcome',
        'Version Booster': 'booster_version',
        'Booster landing': 'booster_landing',
        'Date': 'date',
        'Time': 'time',
    }
    df_web_std = standardize_columns(df_web_clean, web_column_map)

    # Merging along flight_number & keep only the desired columns
    merged_df = pd.merge(
        df_api_std[['flight_number', 'booster', 'payload_mass', 'outcome', 'date', 'longitude', 'latitude', 'reused', 'reused_count', 'serial', 'landing_pad', 'gridfins', 'legs']],
        df_web_std[['flight_number', 'booster_version', 'orbit', 'launch_site']], # 'launch_outcome' not necessary
        on='flight_number',
        how='inner' # keeps only the launches that are present in both frames
    )

    # create 'class' attribute for eda and logistic regression (later)
    df_final = create_class_attribute(merged_df,verbose=True)

    # Save merged & cleaned version for dashboard use
    df_final.to_csv(output_csv, index=False)
    print(f"\nData successfully cleaned and merged.")
    print(f"\nNew dataframe has {df_final.shape[0]} rows and {df_final.shape[1]} columns.")
    print(f"\nData successfully saved to {output_csv} for EDA & dashboard use.")
    print("\nOverview (first ten rows):\n", df_final.head(10))


if __name__ == "__main__":
    main()
