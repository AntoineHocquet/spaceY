import pandas as pd
from src.ml.features import select_features, preprocess_features

# desired_features=['flight_number','booster','payload_mass','orbit',
#                   'launch_site','reused','legs','reused_count','longitude','latitude'] #10

def test_select_features_returns_expected_columns():
    df = pd.DataFrame({
        'flight_number': [1],
        'booster': ['Falcon 9'],
        'payload_mass': [1000],
        'orbit': ['LEO'],
        'launch_site': ['CCAFS'],
        'grid_fins': [True],
        'reused': [False],
        'legs': [True],
        'landing_pad': ['LZ-1'],
        'block': [5],
        'reused_count': [1],
        'serial': ['B1049'],
        'longitude': [0],
        'latitude': [0],
        'extra_column': ['to_drop']
    })
    features = select_features(df)
    assert features.shape[1] == 10
    assert 'extra_column' not in features.columns


def test_preprocess_features_runs():
    df = pd.DataFrame({
        'flight_number': [1],
        'booster': ['Falcon 9'],
        'payload_mass': [1000],
        'orbit': ['LEO'],
        'launch_site': ['CCAFS'],
        'reused': [False],
        'legs': [True],
        'reused_count': [1],
        'longitude': [0],
        'latitude': [0]
    })
    X_transformed, encoder = preprocess_features(df, categorical_cols = ['booster', 'orbit','launch_site'])
    assert hasattr(X_transformed, 'shape')
    # test if X_transformed has only numerical or boolean values
    assert X_transformed.dtypes.apply(lambda x: x in [float, bool]).all()
