import pandas as pd

def preprocess_data(df):

    # Convert categorical to numeric
    df = pd.get_dummies(df, columns=["Source", "Destination"])

    return df