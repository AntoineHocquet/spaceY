import pandas as pd
import sqlite3
from pathlib import Path

def create_database(csv_path: str, db_path: str, table_name="SPACEXTBL"):
    df = pd.read_csv(csv_path)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)

if __name__ == '__main__':
    csv_path = "data/spacex_launch_dash.csv"
    db_path = "data/SpaceX.db"
    
    # Create data folder if not exists
    Path("data").mkdir(exist_ok=True)

    create_database(csv_path, db_path)
    print(f"Database created at {db_path}")
