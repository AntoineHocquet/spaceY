from src.ml.pipeline import create_pipeline
from sklearn.pipeline import Pipeline

def test_create_pipeline_returns_pipeline_object():
    pipeline = create_pipeline(model_type="svm")
    assert isinstance(pipeline, Pipeline)

def test_pipeline_supported_models():
    for model in ["logistic", "decision_tree", "svm", "random_forest"]:
        pipeline = create_pipeline(model_type=model)
        assert isinstance(pipeline, Pipeline)