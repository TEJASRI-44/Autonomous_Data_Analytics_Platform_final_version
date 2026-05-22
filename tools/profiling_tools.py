def generate_dataset_summary(df):

    summary = {

        "rows": df.shape[0],

        "columns": df.shape[1],

        "column_names": list(df.columns),

        "missing_values":
        df.isnull().sum().to_dict(),

        "data_types":
        df.dtypes.astype(str).to_dict()
    }

    return summary