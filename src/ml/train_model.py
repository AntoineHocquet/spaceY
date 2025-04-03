# src/ml/train_model.py
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from src.ml.features import select_features, preprocess_features
from src.ml.pipeline import create_pipeline
from src.ml.model_evaluation import compute_accuracy, plot_confusion_matrix


def train_and_save_model(data_path, model_path="models/model.pkl"):
    """
    Full training pipeline: load data, train model, save artifact.

    Parameters:
    - data_path: str, path to input CSV file (later replaceable by DB call)
    - model_path: str, path to store the trained model
    """
    # 1. Load Data
    df = pd.read_csv(data_path)
    X_raw = select_features(df)
    y = df['class'].astype(float)  # pandas Series for binary classification (1 = success, 0 = fail)

    # 2. Preprocess
    X_processed, encoder = preprocess_features(X_raw)

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. Build & Train Model Pipeline
    pipeline = create_pipeline(model_type="logistic")
    pipeline.fit(X_train, y_train)

    # 5. Evaluate
    y_pred = pipeline.predict(X_test)
    acc = compute_accuracy(y_test, y_pred)
    print(f"Model Accuracy: {acc:.4f}")
    plot_confusion_matrix(y_test, y_pred, labels=["did not land", "landed"],save_path="docs/metrics/confusion_matrix.png")

    # 6. Save model
    joblib.dump((pipeline, encoder), model_path)
    print(f"Model saved to: {model_path}")


if __name__ == "__main__":
    train_and_save_model("data/spacex_launch_dash.csv")
