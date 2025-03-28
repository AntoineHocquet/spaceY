# 🚀 Rocket Science Simplified: Decoding SpaceX Landing Outcomes

**SpaceY** is a fictional company competing with SpaceX. This project predicts whether SpaceX Falcon 9 launches result in successful landings, with the aim of understanding rocket reusability and costs. 

---

## 📊 Project Highlights

- 🔎 **Data Collection**: Web scraping and REST API integration
- 🧹 **Data Wrangling**: Cleaning and merging multi-source datasets
- 📊 **EDA**: SQL queries, seaborn/plotly, geospatial visualization with Folium
- 🤖 **Machine Learning**: Logistic regression for success prediction
- 🖥️ **Dashboard**: Interactive analytics using Dash (Dropdown + Slider + Pie + Scatter)

---

## 🗂️ Repository Structure

spaceY/
├── data/                     # Raw & processed data files
│   └── spacex_launch_dash.csv
├── notebooks/                # All Jupyter notebooks (archived but readable)
│   ├── m1_webscraping.ipynb
│   ├── m1_data-collection-api.ipynb
│   ├── m1_data-wrangling.ipynb
│   ├── m2_eda-sql-coursera_sqllite.ipynb
│   ├── m2_eda-dataviz.ipynb
│   ├── m3_launch_site_location.ipynb
│   ├── m4_machine-learning-prediction.ipynb
├── dashboard/                # Dash app files
│   ├── m3_dashboard.py
│   └── assets/               # For CSS/images (if needed)
├── docs/                     # Images/screenshots for README & presentation
│   └── dashboard_screenshot.png
├── src/                      # Reusable Python scripts
│   └── (e.g., load_data.py, train_model.py, plot_utils.py)
├── models/                   # Trained ML models (.pkl or .joblib)
├── .gitignore
├── README.md
├── requirements.txt
└── Makefile


---

## 🧪 How to Run

### Install requirements:
```bash
pip install -r requirements.txt
```

## 📌 Sample Insights
CCAFS site had the most successful launches

Payloads between 5000–8000 kg had the highest success rate

Booster version B5 had the highest reliability

---

## 🛠 Tech Stack
Python (pandas, numpy, sklearn, plotly, dash, folium)

SQLite3 for SQL-based EDA

Docker-ready structure (MLOps best practices)


---

## 👤 Author
Antoine Hocquet
GitHub Profile | LinkedIn
MIT Applied DS Program • PhD in Applied Mathematics • 8+ years in academia
