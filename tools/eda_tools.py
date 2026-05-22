import pandas as pd


def get_numerical_columns(df):

    return list(

        df.select_dtypes(
            include=["int64", "float64"]
        ).columns

    )
    
def get_categorical_columns(df):

    return list(

        df.select_dtypes(
            include=["object"]
        ).columns

    )
    
import pandas as pd


def get_datetime_columns(df):

    datetime_columns = []

    object_columns = (

        df.select_dtypes(
            include=["object"]
        ).columns

    )

    for column in object_columns:

        try:

            converted = pd.to_datetime(

                df[column],

                errors="raise",

                format="%Y-%m-%d"

            )

            datetime_columns.append(column)

        except Exception:

            pass

    return datetime_columns
def get_boolean_columns(df):

    return list(

        df.select_dtypes(
            include=["bool"]
        ).columns

    )
    
def get_dataset_shape(df):

    return {

        "rows": df.shape[0],

        "columns": df.shape[1]
    }
    
def analyze_missing_values(df):

    return (

        df.isnull()

        .sum()

        .to_dict()

    )
    
def analyze_missing_percentage(df):

    missing_percentage = (

        df.isnull()

        .mean()

        * 100

    )

    return missing_percentage.to_dict()

def detect_duplicate_rows(df):

    duplicates = (

        df.duplicated()

        .sum()

    )

    return int(duplicates)

def generate_summary_statistics(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    return numerical_df.describe().to_dict()
def generate_correlation_matrix(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    correlation_matrix = (

        numerical_df.corr()

    )

    return correlation_matrix.to_dict()
def analyze_unique_values(df):

    unique_values = {}

    for column in df.columns:

        unique_values[column] = (

            df[column].nunique()

        )

    return unique_values

def detect_high_cardinality_columns(df):

    high_cardinality = []

    for column in df.columns:

        if df[column].nunique() > 50:

            high_cardinality.append(column)

    return high_cardinality

def detect_constant_columns(df):

    constant_columns = []

    for column in df.columns:

        if df[column].nunique() == 1:

            constant_columns.append(column)

    return constant_columns

def analyze_skewness(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    skewness = (

        numerical_df.skew()

    )

    return skewness.to_dict()


def detect_outliers(df):

    numerical_columns = (

        df.select_dtypes(
            include=["int64", "float64"]
        ).columns

    )

    outlier_summary = {}

    for column in numerical_columns:

        q1 = df[column].quantile(0.25)

        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr

        upper = q3 + 1.5 * iqr

        outliers = df[

            (df[column] < lower)

            |

            (df[column] > upper)

        ]

        outlier_summary[column] = len(outliers)

    return outlier_summary

def analyze_memory_usage(df):

    memory = (

        df.memory_usage(
            deep=True
        ).sum()

    )

    return int(memory)



