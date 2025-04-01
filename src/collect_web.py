# src/collect_web.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
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


def extract_date_time(table_cell):
    """
    Extract the date and time from an HTML table cell.
    
    Args:
        table_cell: An element of a table data cell containing date and time information.
        
    Returns:
        A list containing the date and time as strings.
    """
    return [element.strip() for element in table_cell.strings][:2]


def extract_booster_version(table_cells):
    """
    Extract the booster version from an HTML table cell.

    Args:
        table_cells: An element of a table data cell containing booster version information.

    Returns:
        A string containing the booster version.
    """
    booster_versions = [version for i, version in enumerate(table_cells.strings) if i % 2 == 0]
    return ''.join(booster_versions[:-1])


def extract_landing_status(table_cells):
    """
    Extract the landing status from an HTML table cell.
    
    Args:
        table_cells: An element of a table data cell containing landing status information.
        
    Returns:
        A string containing the landing status.
    """
    return list(table_cells.strings)[0]


def extract_mass(table_cells):
    """
    Extract mass from an HTML table cell.
    
    Args:
        table_cells: An element of a table data cell containing mass information.
        
    Returns:
        A string containing the mass.
    """
    mass_str = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass_str:
        mass_str = mass_str[: mass_str.find("kg") + 2]
    else:
        mass_str = "0 kg"
    return mass_str


def extract_column_from_header(row):
    """
    Extract and clean the column name from an HTML table row element.
    
    Args:
        row: A BeautifulSoup Tag object representing a table row.
        
    Returns:
        A string containing the cleaned column name.
    """
    # Remove unwanted HTML tags
    for unwanted in ['br', 'a', 'sup']:
        tag = row.find(unwanted)
        if tag:
            tag.extract()
    
    # Extract and clean the column name
    column_name = ' '.join(row.contents).strip()
    
    # Filter out numeric and empty names
    if not column_name.isdigit():
        return column_name


def parse_launch_table(html, table_index=2, return_soup=False):
    """
    Parse launch data table from SpaceX Wikipedia page.

    Args:
        html: The HTML content of the SpaceX Wikipedia page.
        table_index: The index of the table to parse (default is 2).
        return_soup: Whether to return the BeautifulSoup object (default is False).

    Returns:
        A list of dictionaries containing launch data if `return_soup` is False, otherwise a tuple of a list of dictionaries and a BeautifulSoup object.
    """
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table")

    selected_table = tables[table_index]
    column_names = []

    header_elements = selected_table.find_all(name='th')

    for header in header_elements:
        column_name = extract_column_from_header(header)
        if column_name:
            column_names.append(column_name)

    if return_soup:
        return column_names, soup
    return column_names


def save_scraped_data_to_csv(scraped_data: pd.DataFrame, output_file_path: str) -> None:
    """
    Save scraped data to a CSV file.

    Args:
        scraped_data: The scraped data as a pandas DataFrame.
        output_file_path: The path to save the CSV file to.
    """
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    scraped_data.to_csv(output_file_path, index=False)


def main():
    config = load_config()
    url = config["spacex_wikipedia_url"]
    output_file_path = os.path.join(config["output_dir"], config["web_output_file"])

    html = fetch_html(url)
    scraped_data = parse_launch_table(html)
    save_scraped_data_to_csv(scraped_data, output_file_path)

if __name__ == "__main__":
    main()
