# src/collect_web.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def fetch_html(url: str) -> str:
    """
    Fetch raw HTML content from a given URL.
    """
    print(f"Fetching HTML from {url}")
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_launch_table(html: str) -> pd.DataFrame:
    """
    Parse launch data table from SpaceX Wikipedia page.
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    # This might change depending on the source; adjust as needed
    tables = soup.find_all("table", {"class": "wikitable"})
    print(f"Found {len(tables)} wikitable(s)")

    # Relevant table
    INDEX_LAUNCH_DATA=1
    df = pd.read_html(str(tables[INDEX_LAUNCH_DATA]))[0]
    print(f"Extracted {len(df)} rows from HTML table.")
    return df


def save_to_csv(df: pd.DataFrame, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved scraped data to {output_path}")

def main():
    url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
    output_csv = "data/spacex_web_data.csv"

    html = fetch_html(url)
    df = parse_launch_table(html)
    save_to_csv(df, output_csv)

if __name__ == "__main__":
    main()
