# This module contains SQL queries used for exploratory data analysis (EDA)
## on the SpaceX launch dataset stored in a SQLite database.
### It provides reusable functions for querying data such as launch statistics,
#### success rates, and booster version analysis.
##### Author: SpaceY Project - Antoine Hocquet / IBM

import sqlite3
import pandas as pd


def run_query(database_path: str, query: str) -> pd.DataFrame:
    """
    Execute a SQL query and return the result as a pandas DataFrame.
    
    Parameters:
    - database_path (str): Path to the SQLite database file.
    - query (str): SQL query to execute.
    
    Returns:
    - pd.DataFrame: Query results.
    """
    with sqlite3.connect(database_path) as conn:
        return pd.read_sql_query(query, conn)


# === Predefined Queries === #

def get_all_launches():
    return """
    SELECT * FROM SPACEXTBL;
    """


def get_unique_boosters():
    return """
    SELECT DISTINCT booster_version FROM SPACEXTBL;
    """


def get_total_payload_by_site():
    return """
    SELECT launch_site, SUM(payload_mass) AS total_payload
    FROM SPACEXTBL
    GROUP BY launch_site;
    """


def get_successful_launches_by_site():
    return """
    SELECT launch_site, SUM(class) AS successful_launches
    FROM SPACEXTBL
    GROUP BY launch_site;
    """


def get_max_payload_site():
    return """
    SELECT launch_site, MAX(payload_mass) AS max_payload
    FROM SPACEXTBL
    GROUP BY launch_site
    ORDER BY max_payload DESC
    LIMIT 1;
    """


def get_avg_success_by_site():
    return """
    SELECT launch_site, AVG(class) AS success_rate
    FROM SPACEXTBL
    GROUP BY launch_site
    ORDER BY success_rate DESC;
    """


def get_success_rate_by_booster():
    return """
    SELECT booster_version, AVG(class) AS success_rate
    FROM SPACEXTBL
    GROUP BY booster_version
    ORDER BY success_rate DESC;
    """


def get_success_rate_by_payload_range(min_payload: float, max_payload: float):
    return f"""
    SELECT payload_mass, class
    FROM SPACEXTBL
    WHERE payload_mass BETWEEN {min_payload} AND {max_payload};
    """


# Run queries directly for debugging
if __name__ == '__main__':
    db_path = "data/SpaceX.db"
    query = get_successful_launches_by_site()
    print(run_query(db_path, query))
