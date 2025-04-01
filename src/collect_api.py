# src/collect_api.py

import requests
import pandas as pd
import os
import datetime
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
    data = pd.json_normalize(launches)

    # Keeping only the features we want and the flight number, and date_utc.
    data = data[['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']]

    # Remove rows with multiple cores because those are falcon rockets with 2 extra rocket boosters and rows that have multiple payloads in a single rocket.
    data = data[data['cores'].map(len)==1]
    data = data[data['payloads'].map(len)==1]

    # Since payloads and cores are lists of size 1 we will also extract the single value in the list and replace the feature.
    data['cores'] = data['cores'].map(lambda x : x[0])
    data['payloads'] = data['payloads'].map(lambda x : x[0])

    # We also want to convert the date_utc to a datetime datatype and then extracting the date leaving the time
    data['date'] = pd.to_datetime(data['date_utc']).dt.date
    
    # Using the date we will restrict the dates of the launches
    data = data[data['date'] <= datetime.date(2020, 11, 13)]
    print(f"Retrieved {len(data)} launches.")
    return data

def get_booster_version(data):
    """
    Takes the dataset and uses the rocket column to call the API and append the data to the BoosterVersion list
    """
    BoosterVersion=[]
    for rocket_id in data['rocket']:
        if rocket_id:
            response = requests.get(f"https://api.spacexdata.com/v4/rockets/{rocket_id}").json()
            BoosterVersion.append(response.get('name'))
    print(f"Obtained successfully {len(BoosterVersion)} Booster Versions")
    return BoosterVersion

def get_launch_site_info(data):
    """
    Retrieve launch site data from API and append to lists
    """
    longitude_list = []
    latitude_list = []
    launch_site_list = []
    for launchpad_id in data['launchpad']:
        if launchpad_id:
            response = requests.get(f"https://api.spacexdata.com/v4/launchpads/{launchpad_id}").json()
            longitude_list.append(response['longitude'])
            latitude_list.append(response['latitude'])
            launch_site_list.append(response['name'])
    print(f"Obtained successfully {len(launch_site_list)} Launch Sites")
    return longitude_list, latitude_list, launch_site_list

def get_payload_data(data):
    """
    Takes the dataset and uses the payloads column to call the API and append the data to the lists
    """
    payload_mass_list = []
    orbit_list = []
    for payload in data['payloads']:
        if payload:
            response = requests.get(f"https://api.spacexdata.com/v4/payloads/{payload}").json()
            payload_mass_list.append(response.get('mass_kg'))
            orbit_list.append(response.get('orbit'))
    print(f"Obtained successfully {len(payload_mass_list)} Payloads")
    return payload_mass_list, orbit_list

def get_core_data(data):
    """
    Takes the dataset and uses the cores column to call the API and append the data to the lists
    """
    block_list = []
    reused_count_list = []
    serial_list = []
    outcome_list = []
    flights_list = []
    gridfins_list = []
    reused_list = []
    legs_list = []
    landing_pad_list = []
    for core in data['cores']:
        if core['core'] is not None:
            response = requests.get(f"https://api.spacexdata.com/v4/cores/{core['core']}").json()
            block_list.append(response['block'])
            reused_count_list.append(response['reuse_count'])
            serial_list.append(response['serial'])
        else:
            block_list.append(None)
            reused_count_list.append(None)
            serial_list.append(None)
        outcome_list.append(
            f"{core['landing_success']} {core['landing_type']}"
        )
        flights_list.append(core['flight'])
        gridfins_list.append(core['gridfins'])
        reused_list.append(core['reused'])
        legs_list.append(core['legs'])
        landing_pad_list.append(core['landpad'])
    print(f"Obtained successfully {len(block_list)} Cores")
    return (
        block_list,
        reused_count_list,
        serial_list,
        outcome_list,
        flights_list,
        gridfins_list,
        reused_list,
        legs_list,
        landing_pad_list,
    )

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
    
    data = fetch_spacex_launch_data(api_url)
    data['BoosterVersion'] = get_booster_version(data)
    longitude_list, latitude_list, launch_site_list = get_launch_site_info(data)
    payload_mass_list, orbit_list = get_payload_data(data)
    block_list, reused_count_list, serial_list, outcome_list, flights_list, gridfins_list, reused_list, legs_list, landing_pad_list = get_core_data(data)
    data['longitude'] = longitude_list
    data['latitude'] = latitude_list
    data['launch_site'] = launch_site_list
    data['payload_mass'] = payload_mass_list
    data['orbit'] = orbit_list
    data['block'] = block_list
    data['reused_count'] = reused_count_list
    data['serial'] = serial_list
    data['outcome'] = outcome_list
    data['flights'] = flights_list
    data['gridfins'] = gridfins_list
    data['reused'] = reused_list
    data['legs'] = legs_list
    data['landing_pad'] = landing_pad_list
    df = pd.DataFrame(data)
    save_to_csv(df, output_path)

if __name__ == "__main__":
    main()
