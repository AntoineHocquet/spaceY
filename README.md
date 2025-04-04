# 🚀 Rocket Science Simplified: Decoding SpaceX Landing Outcomes

**SpaceY** is a fictional company competing with SpaceX. This project predicts whether SpaceX Falcon 9 launches result in successful landings, with the aim of understanding rocket reusability and costs. Built with production-ready Python pipelines and MLOps practices.

---

## 📊 Project Highlights

- 🔎 **Data Collection**: Web scraping and REST API integration
- 🧹 **Data Wrangling**: Cleaning and merging multi-source datasets
- 📊 **EDA**: SQL queries, seaborn/plotly, geospatial visualization with Folium
- 🤖 **Machine Learning**: Logistic regression, decision trees, SVM, and random forest
- 🖥️ **Dashboard**: Interactive analytics using Dash (Dropdown + Slider + Pie + Scatter)
- 🧪 **Testing**: Unit tests with pytest
- 🛠️ **CLI Interface**: Unified `cli.py` for training, EDA, and dashboard control
- ⚙️ **Automation**: Makefile targets for quick reproducibility

---

## 🗂️ Repository Structure

```
spaceY/
├── cli.py                    # Unified CLI for training, EDA, dashboard
├── data/                     # Raw & processed data files
│   └── spacex_launch_dash.csv
├── models/                   # Trained ML models (.pkl or .joblib)
├── notebooks/                # Archived notebooks (web, API, EDA, ML)
├── docs/                     # Screenshots or auto-generated EDA outputs
├── src/                      # Modular Python scripts
│   ├── clean_merge.py
│   ├── collect_api.py
│   ├── collect_web.py
│   ├── ml/                   # ML pipeline modules (features, train, pipeline, eval)
│   ├── eda/                  # EDA scripts and dashboard
│   └── utils/                # Config loaders, DB utils
├── tests/                    # Unit tests
├── requirements.txt          # Python dependencies
├── Makefile                  # Dev & pipeline automation
└── README.md
```

---

## 🧪 How to Run

### 🔧 Install dependencies:
```bash
pip install -r requirements.txt
```

### ⚙️ Run data pipeline:
```bash
make run-ETL
```

### 🚀 Train ML models:
```bash
make train-logistic           # Logistic Regression
make train-decision-tree
make train-svm
make train-random-forest
make train-all                # Trains all models
```

### 📦 Or use the CLI:
```bash
python cli.py train --model svm
python cli.py dashboard
python cli.py eda
```

---

## 📌 Sample Insights

- 🛰️ CCAFS site had the most successful launches
- ⚖️ Payloads between 5000–8000 kg had the highest success rate
- 🔧 Booster version B5 had the highest reliability

---

## 🛠 Tech Stack

- Python (pandas, numpy, sklearn, plotly, dash, folium)
- SQLite3 for SQL-based EDA
- CLI: `argparse`
- Testing: `pytest`
- Automation: `Makefile`

---

## 👤 Author
Antoine Hocquet  
[GitHub](https://github.com/AntoineHocquet) • [LinkedIn](https://www.linkedin.com/in/antoine-hocquet/)  
MIT Applied DS Program • PhD in Applied Mathematics • 8+ years in academia

---

## 🚨 Note

This project was inspired by the "IBM Data Science" Coursera specialization.  
Certain parts (e.g., dashboard instructions and dataset) were adapted from educational labs © IBM Corporation.
