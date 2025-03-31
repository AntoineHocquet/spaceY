# tests/test_collect_api.py

from src.collect_api import fetch_spacex_launch_data

def test_api_columns_exist():
    df = fetch_spacex_launch_data("https://api.spacexdata.com/v4/launches")
    required_columns = {'name', 'date_utc', 'rocket', 'success', 'payloads', 'launchpad'}
    assert required_columns.issubset(df.columns), f"Missing columns: {required_columns - set(df.columns)}"
