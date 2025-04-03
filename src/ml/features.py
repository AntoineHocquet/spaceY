# src/ml/features.py
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

#DESIRED_FEATURES=['flight_number','booster','payload_mass','orbit','launch_site','reused','legs','landing_pad','reused_count','longitude','latitude','class']
## removed for now: 'serial', 'landing_pad', 'date', 'flights','grid_fins', 'block',
### removed permanently: 'outcome' (also: 'class' which is the dependent variable)

def select_features(df, desired_features=['flight_number','booster',
                                          'payload_mass','orbit','launch_site',
                                          'reused','legs','reused_count',
                                          'longitude','latitude']):
    """
    Select relevant features from the input dataframe.
    """
    XX=df[desired_features].copy()
    return XX


def preprocess_features(XX, categorical_cols = ['booster', 'orbit','launch_site']): #, 'launch_site', 'landing_pad', 'serial'
    """
    Encode categorical features and fill missing values.
    Returns the transformed feature matrix and fitted transformer.
    """
    # One-hot encode categorical variables
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
        ],
        remainder='passthrough'
    )
    XXX = preprocessor.fit_transform(XX).astype(float)
    # Get new column names and remove "cat__" & "remainder__" prefixes
    ## Note: can be done with optional arg 'verbose_feature_names_out=False for sklearn>=1.3' in ColumnTransformer()
    new_columns = [name.split("__")[-1] for name in preprocessor.get_feature_names_out()]
    X_transformed = pd.DataFrame(XXX, columns=new_columns)

    return X_transformed, preprocessor


if __name__=='__main__':
    X = pd.read_csv("data/spacex_launch_dash.csv")
    XX=select_features(X)
    y= X['class']
    X_transformed, _ = preprocess_features(XX)

    print(X_transformed)
    print(type(y))
    print(y)