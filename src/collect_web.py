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


def extract_column_name_from_header(row):
    """
    Extract and clean the column name from an HTML table row element.
    
    Args:
        row: A BeautifulSoup Tag object representing a table row.
        
    Returns:
        A string containing the cleaned column name.
    """
    # Remove unwanted HTML tags
    for unwanted in ['br', 'a', 'sup']:
        for tag in row.find_all(unwanted):
            tag.decompose()

    # Extract and clean the column name
    column_name = ' '.join(
        str(content).strip() for content in row.contents
        if isinstance(content, str) or content.name is None
    ).strip()

    # Filter out numeric and empty names    
    if column_name and not column_name.isdigit():
        return column_name
    return None


def extract_table_headers(html, table_index=2, return_soup=False):
    """
    Extract cleaned column names from a specific HTML table.
    """
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all("table")
    selected_table = tables[table_index]
    
    header_elements = selected_table.find_all('th')
    column_names = [
        extract_column_name_from_header(header)
        for header in header_elements
        if extract_column_name_from_header(header)
    ]
    
    return (column_names, soup) if return_soup else column_names


def parse_soup_table(column_names, soup):
    """
    Parse a BeautifulSoup object and extract launch data from its tables.
    """
    
    # create empty dictionary with keys from the extracted column names in the previous task
    launch_dict= dict.fromkeys(column_names)

    # Remove irrelevant column
    del launch_dict['Date and time ( )']

    # Initialize the launch_dict with each value to be an empty list
    launch_dict['Flight No.'] = []
    launch_dict['Launch site'] = []
    launch_dict['Payload'] = []
    launch_dict['Payload mass'] = []
    launch_dict['Orbit'] = []
    launch_dict['Customer'] = []
    launch_dict['Launch outcome'] = []

    # Add some new columns
    launch_dict['Version Booster']=[]
    launch_dict['Booster landing']=[]
    launch_dict['Date']=[]
    launch_dict['Time']=[]

    # NEXT: Fill up the `launch_dict` with launch records extracted from table rows
    extracted_row = 0
    print(f"Found {len(soup.find_all('table'))} tables on the page")
    #Extract each table 
    for table_number,table in enumerate(soup.find_all('table',"wikitable plainrowheaders collapsible")):
        #print(f"Extracting table {table_number} out of {len(soup.find_all('table','wikitable plainrowheaders collapsible'))}")
        # get table row 
        for rows in table.find_all("tr"):
            #check to see if first table heading is as number corresponding to launch a number 
            if rows.th:
                if rows.th.string:
                    flight_number=rows.th.string.strip()
                    flag=flight_number.isdigit()
            else:
                flag=False
            #get table element 
            row=rows.find_all('td')
            #if it is number save cells in a dictonary 
            if flag:
                extracted_row += 1
                # Flight Number value
                launch_dict['Flight No.'].append(flight_number)
                
                datatimelist = extract_date_time(row[0])
            
                # Date value
                date = datatimelist[0].strip(',')
                launch_dict['Date'].append(date)
                print(date)
            
                # Time value
                time = datatimelist[1]
                launch_dict['Time'].append(date)
              
                # Booster version
                bv=extract_booster_version(row[1])
                if not(bv):
                    bv=row[1].a.string
                launch_dict['Version Booster'].append(bv)
            
                # Launch Site
                launch_site = row[2].a.string
                launch_dict['Launch site'].append(launch_site)
            
                # Payload
                payload = row[3].a.string
                launch_dict['Payload'].append(payload)
            
                # Payload Mass
                payload_mass = extract_mass(row[4])
                launch_dict['Payload mass'].append(payload_mass)
            
                # Orbit
                orbit = row[5].a.string
                launch_dict['Orbit'].append(orbit)
            
                # Customer
                customer = row[6].a.string if row[6].a else row[6].string
                launch_dict['Customer'].append('customer')
            
                # Launch outcome
                launch_outcome = list(row[7].strings)[0]
                launch_dict['Launch outcome'].append(launch_outcome)
            
                # Booster landing
                booster_landing = extract_landing_status(row[8])
                launch_dict['Booster landing'].append('booster_landing')

            print(f"{extracted_row} records extracted")

    return launch_dict


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
    static_url =config["spacex_wikipedia_url_static"]
    output_file_path = os.path.join(config["output_dir"], config["web_output_file"])

    html = fetch_html(static_url)
    column_names, soup = extract_table_headers(html, return_soup=True)
    print(column_names)

    launch_dict = parse_soup_table(column_names, soup)
    df= pd.DataFrame({ key:pd.Series(value) for key, value in launch_dict.items() })
    save_scraped_data_to_csv(df, output_file_path)
    print(f"Scraped data saved to {output_file_path}")

if __name__ == "__main__":
    main()
