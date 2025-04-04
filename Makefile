# Makefile for the SpaceY MLOps project

# === General commands ===
help:
	@echo "Available commands:"
	@echo "  make collect-api     - Run the SpaceX API data collection"
	@echo "  make collect-web     - Run the web scraping script"
	@echo "  make clean-merge     - Clean and merge data for EDA, dashboard and ML"
	@echo "  make run-ETL         - Run the full Extract-Load-Transform pipeline (API + Web + Clean&Merge)"
	@echo "  make test            - Run all unit tests with pytest"
	@echo "  make lint            - Run code style check with flake8"
	@echo "  make train-logistic       - Train logistic model on launch data"
	@echo "  make train-decision-tree  - Train decision tree model on launch data"
	@echo "  make train-svm            - Train support vector machine model on launch data"
	@echo "  make train-random-forest  - Train random forest model on launch data"
	@echo "  make train-all            - Train all models sequentially"

# === Pipeline commands ===
collect-api:
	PYTHONPATH=. python src/collect_api.py

collect-web:
	PYTHONPATH=. python src/collect_web.py

clean-merge:
	PYTHONPATH=. python src/clean_merge.py

create-db:
	PYTHONPATH=. python src/utils/create_db_from_csv.py

dashboard:
	PYTHONPATH=. python src/eda/dashboard.py

run-ETL: collect-api collect-web clean-merge create-db

# === Dev tools ===
test:
	PYTHONPATH=. pytest -v

lint:
	flake8 src/ tests/

# === ML Training Commands ===
train-logistic:
	PYTHONPATH=. python src/ml/train_model.py --model logistic --data spacex_launch_dash.csv

train-decision-tree:
	PYTHONPATH=. python src/ml/train_model.py --model decision_tree --data spacex_launch_dash.csv

train-svm:
	PYTHONPATH=. python src/ml/train_model.py --model svm --data spacex_launch_dash.csv

train-random-forest:
	PYTHONPATH=. python src/ml/train_model.py --model random_forest --data spacex_launch_dash.csv

train-all: train-logistic train-decision-tree train-svm train-random-forest

# === CLI Wrappers ===
cli-train:
	PYTHONPATH=. python cli.py train --model logistic --data data/spacex_launch_dash.csv

cli-dashboard:
	PYTHONPATH=. python cli.py dashboard

cli-eda:
	PYTHONPATH=. python cli.py eda

