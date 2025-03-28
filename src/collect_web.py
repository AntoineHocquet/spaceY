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

# def parse_launch_table(html: str) -> pd.DataFrame:
#     """
#     Parse launch data table from SpaceX Wikipedia page.
#     """
#     soup = BeautifulSoup(html, 'html.parser')
    
#     # This might change depending on the source; adjust as needed
#     tables = soup.find_all("table", {"class": "wikitable"})
#     print(f"Found {len(tables)} wikitable(s)")

#     # Assume first relevant table
#     df = pd.read_html(str(tables[0]))[0]
#     print(f"Extracted {len(df)} rows from HTML table.")
#     return df

def parse_launch_table(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table", {"class": "wikitable"})
    print(f"Found {len(tables)} wikitable(s)")

    # Preview table structures
    for i, table in enumerate(tables):
        print(f"\n--- Table {i} preview ---")
        try:
            df = pd.read_html(str(table))[0]
            print(df.head(2))
        except Exception as e:
            print(f"Could not parse table {i}: {e}")
    
    return pd.read_html(str(tables[YOUR_INDEX_HERE]))[0]


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
