import pandas as pd

def load_dataset(file_path):

    if file_path.endswith(".csv"):
        
        df = pd.read_csv(file_path)
        
    elif file_path.endswith(".xlsx"):
        
        df = pd.read_excel(file_path)
        
    return df