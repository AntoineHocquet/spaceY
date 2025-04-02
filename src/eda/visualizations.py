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


def plot_booster_versions(df):
    plt.figure(figsize=(12, 6))
    sns.countplot(data=df, x='booster_version', order=df['booster_version'].value_counts().index)
    plt.title("Booster Version Category Counts")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(DOCS_PATH / "booster_version_counts.png")
    plt.close()


def plot_payload_vs_success(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='payload_mass', y='class', hue='booster_version')
    plt.title("Payload vs. Success")
    plt.savefig(DOCS_PATH / "payload_vs_success.png")
    plt.close()


def run_all():
    df = load_data()
    plot_landing_distribution(df)
    plot_booster_versions(df)
    plot_payload_vs_success(df)
    print(f"Plots saved to {DOCS_PATH.resolve()}")


if __name__ == "__main__":
    run_all()
