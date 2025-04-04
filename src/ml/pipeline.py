# src/ml/pipeline.py
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

def create_pipeline(model_type="logistic", **kwargs):
    """
    Create a scikit-learn pipeline with optional model type.

    Args:
    - model_type: "logistic" (default), "decision_tree", "svm" or "random_forest"
    - kwargs: model-specific hyperparameters

    Returns:
    - sklearn.pipeline.Pipeline object
    """
    if model_type == "logistic":
        model = LogisticRegression(**kwargs)
    elif model_type == "decision_tree":
        model = DecisionTreeClassifier(**kwargs)
    elif model_type == "svm":
        model = SVC(**kwargs)
    elif model_type == "random_forest":
        model = RandomForestClassifier(**kwargs)
    else:
        raise ValueError(f"Unsupported model_type: {model_type}")

    pipeline = Pipeline([
        ('scaler', StandardScaler(with_mean=False)),  # with_mean=False for sparse input after OneHotEncoder
        ('classifier', model)
    ])

    return pipeline
