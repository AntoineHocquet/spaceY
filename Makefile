# Makefile for the SpaceY MLOps project

# === General commands ===
help:
	@echo "Available commands:"
	@echo "  make collect-api     - Run the SpaceX API data collection"
	@echo "  make collect-web     - Run the web scraping script"
	@echo "  make clean-merge     - Clean and merge data for dashboard/ML"
	@echo "  make test            - Run all unit tests with pytest"
	@echo "  make lint            - Run code style check with flake8"
	@echo "  make run-all         - Run the full data pipeline (API + Web + Merge)"

# === Pipeline commands ===
collect-api:
	PYTHONPATH=. python src/collect_api.py

collect-web:
	PYTHONPATH=. python src/collect_web.py

clean-merge:
	PYTHONPATH=. python src/clean_merge.py

create-db:
	PYTHONPATH=. python src/utils/create_db_from_csv.py

run-all: collect-api collect-web clean-merge

# === Dev tools ===
test:
	PYTHONPATH=. pytest -v

lint:
	flake8 src/ tests/

