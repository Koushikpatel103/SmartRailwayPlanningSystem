import pandas as pd

def load_data(path):
    """
    Load railway dataset
    """
    df = pd.read_csv(path)
    return df