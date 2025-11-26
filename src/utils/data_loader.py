import pandas as pd

def load_csv(path, date_col):
    df = pd.read_csv(path)
    df[date_col] = pd.to_datetime(df[date_col])
    return df
