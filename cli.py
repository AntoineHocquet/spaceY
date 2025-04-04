# cli.py
import argparse
import os
from src.ml.train_model import train_and_save_model
from src.eda.dashboard import launch_dashboard


def run_train(args):
    train_and_save_model(
        csv_file=args.data,
        model_name=args.model
    )

def run_dashboard(_):
    launch_dashboard()

def run_eda(_):
    print("Running EDA: generating static visualizations...")
    from src.eda.visualizations import generate_all
    generate_all()


def main():
    parser = argparse.ArgumentParser(description="SpaceY CLI: Run ML, EDA, or Dashboard modules")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # === train subcommand ===
    train_parser = subparsers.add_parser("train", help="Train a machine learning model")
    train_parser.add_argument("--data", type=str, default="spacex_launch_dash.csv")
    train_parser.add_argument("--model", type=str, default="logistic",
                              choices=["logistic", "decision_tree", "svm", "random_forest"])
    train_parser.set_defaults(func=run_train)

    # === dashboard subcommand ===
    dash_parser = subparsers.add_parser("dashboard", help="Launch interactive Dash app")
    dash_parser.set_defaults(func=run_dashboard)

    # === eda subcommand ===
    eda_parser = subparsers.add_parser("eda", help="Generate EDA plots to docs/ directory")
    eda_parser.set_defaults(func=run_eda)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
