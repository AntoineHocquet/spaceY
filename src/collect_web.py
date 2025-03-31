# src/collect_web.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from src.utils.config_loader import load_config


def fetch_html(url: str) -> str:
    """
    Fetch raw HTML content from a given URL.
    """
    print(f"Fetching HTML from {url}")
    
    # Use requests.get() method with the provided url
    ## and assign the output to a 'response' variable
    response = requests.get(url)
    response.raise_for_status()

    # returns raw html (text) of the response object
    return response.text

def parse_launch_table(html: str, return_soup: bool=False) -> pd.DataFrame:
    """
    Parse launch data table from SpaceX Wikipedia page.
    """
    # Use BeautifulSoup() to create a BeautifulSoup object from a response.text content (raw html)
    soup = BeautifulSoup(html, 'html.parser')
    
    tables = soup.find_all("table", {"class": "wikitable"})
    print(f"Found {len(tables)} wikitable(s)")

    # Relevant table for our purposes
    INDEX_LAUNCH_DATA=1
    df = pd.read_html(str(tables[INDEX_LAUNCH_DATA]))[0]
    print(f"Extracted {len(df)} rows from HTML table.")

    if return_soup: # for testing purposes
        return df, soup
    return df


def save_to_csv(df: pd.DataFrame, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved scraped data to {output_path}")

def main():
    config = load_config()
    web_url = config["spacex_wikipedia_url"]
    output_path = os.path.join(config["output_dir"], config["web_output_file"])

    html = fetch_html(url)
    df = parse_launch_table(html)
    save_to_csv(df, output_path)

if __name__ == "__main__":
    main()
