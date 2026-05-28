import os
import pandas as pd


def validate_dataset(file_path):


    if not os.path.exists(file_path):

        raise FileNotFoundError(
            "Dataset file not found"
        )


    valid_extensions = [
        ".csv",
        ".xlsx"
    ]

    if not any(

        file_path.endswith(ext)

        for ext in valid_extensions
    ):

        raise ValueError(
            "Unsupported file format"
        )

    return True


def validate_dataframe_structure(df):



    if df.empty:

        raise ValueError(
            "Dataset is empty"
        )


    if len(df.columns) < 2:

        raise ValueError(

            "Dataset appears "
            "unstructured or malformed"
        )


    unnamed_columns = [

        col for col in df.columns

        if "unnamed" in str(col).lower()
    ]

    if len(unnamed_columns) > 3:

        raise ValueError(

            "Dataset contains excessive "
            "unnamed columns and appears "
            "semi-structured"
        )


    missing_ratio = (

        df.isnull()
        .sum()
        .sum()
        /
        (df.shape[0] * df.shape[1])
    )

    if missing_ratio > 0.7:

        raise ValueError(

            "Dataset contains excessive "
            "missing values and may "
            "be unstructured"
        )

    constant_columns = [

        col for col in df.columns

        if df[col].nunique() <= 1
    ]

    if len(constant_columns) > (

        len(df.columns) * 0.7
    ):

        raise ValueError(

            "Dataset contains insufficient "
            "structured information"
        )

    return True