# src/visualizations.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Constants
DATA_PATH = Path("data/spacex_launch_dash.csv")
DOCS_PATH = Path("docs/eda_outputs")
DOCS_PATH.mkdir(parents=True, exist_ok=True)


def load_data():
    return pd.read_csv(DATA_PATH)


def plot_landing_distribution(df):
    plt.figure(figsize=(8, 6))
    sns.countplot(data=df, x='class')
    plt.title("Landing Outcome Distribution")
    plt.xlabel("Landing Outcome (1 = Success, 0 = Failure)")
    plt.ylabel("Count")
    plt.savefig(DOCS_PATH / "landing_outcome_distribution.png")
    plt.close()


# def plot_booster_versions(df):
#     plt.figure(figsize=(12, 6))
#     sns.countplot(data=df, x='booster_version', order=df['booster_version'].value_counts().index)
#     plt.title("Booster Version Category Counts")
#     plt.xticks(rotation=45)
#     plt.tight_layout()
#     plt.savefig(DOCS_PATH / "booster_version_counts.png")
#     plt.close()


# def plot_payload_vs_success(df):
#     plt.figure(figsize=(10, 6))
#     sns.scatterplot(data=df, x='payload_mass', y='class', hue='booster_version')
#     plt.title("Payload vs. Success")
#     plt.savefig(DOCS_PATH / "payload_vs_success.png")
#     plt.close()

def plot_payload_vs_success(df):
    plt.figure(figsize=(10, 6))
    sns.catplot(y='payload_mass', x='flight_number', hue="class", data=df, aspect = 5)
    plt.xlabel("Flight Number",fontsize=20)
    plt.ylabel("Pay load Mass (kg)",fontsize=20)
    plt.savefig(DOCS_PATH / "payload_mass_vs_flight_number.png")
    plt.close()


def plot_launch_site_vs_flight_number(df):
    plt.figure(figsize=(10, 6))
    sns.catplot(y="launch_site", x="flight_number", hue="class", data=df, aspect = 5)
    plt.xlabel("Flight Number",fontsize=20)
    plt.ylabel("Launch Site",fontsize=20)
    plt.savefig(DOCS_PATH / "launch_site_vs_flight_number.png")
    plt.close()


def plot_launch_site_vs_payload_mass(df):
    plt.figure(figsize=(10, 6))
    sns.catplot(y="launch_site", x="payload_mass", hue="class", data=df)
    plt.xlabel("Payload Mass (kg)")
    plt.ylabel("Launch Site")
    plt.savefig(DOCS_PATH / "launch_site_vs_payload_mass.png")
    plt.close()


def plot_success_rate_vs_orbit(df):
    plt.figure(figsize=(10, 6))
    df1=pd.DataFrame(df.groupby('Orbit')['Class'].mean())
    sns.barplot(data=df1,x='orbit',y='class',hue='class')
    plt.xlabel('Type of orbit')
    plt.ylabel('Success rate')
    plt.savefig(DOCS_PATH / "success_rate_vs_orbit.png")
    plt.close()


def plot_orbit_vs_flight_number(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(y="orbit", x="flight_number", hue="class", data=df)
    plt.xlabel("Flight Number")
    plt.ylabel("Orbit")
    plt.savefig(DOCS_PATH / "orbit_vs_flight_number.png")
    plt.close()


def plot_orbit_vs_payload_mass(df):
    plt.figure(figsize=(10, 6))
    sns.catplot(x="PayloadMass", y="Orbit", hue="Class", data=df)
    plt.xlabel("Pay load Mass (kg)")
    plt.ylabel("Orbit")
    plt.savefig(DOCS_PATH / "orbit_vs_payload_mass.png")
    plt.close()


def extract_year_from_date(df):
    """
    A simple function to extract years from the date_utc column
    Args: df A dataframe with a date_utc column
    Returns: same dataframe with a year column
      """
    df['year'] = df['date_utc'].str.slice(0, 4)
    return df


# Plot a line chart with x axis to be the extracted year and y axis to be the success rate
def plot_success_rate_vs_year(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="year", y="class", data=pd.DataFrame(df.groupby('year')['class'].mean()))
    plt.xlabel("Year")
    plt.ylabel("Success rate")
    plt.savefig(DOCS_PATH / "success_rate_vs_year.png")
    plt.close()

# ============================================================================
def generate_all():
    df = load_data()
    plot_landing_distribution(df)
    plot_booster_versions(df)
    plot_payload_vs_success(df)
    print(f"Plots saved to {DOCS_PATH.resolve()}")


if __name__ == "__main__":
    # generate_all()
    df= pd.read_csv(DATA_PATH)
    df1=extract_year_from_date(df)
    print(df1.head())
    plot_success_rate_vs_year(df1)
