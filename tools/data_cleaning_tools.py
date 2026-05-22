import pandas as pd


def handle_missing_values(df):

    cleaned_df = df.copy()

    numerical_columns = cleaned_df.select_dtypes(

        include=["int64", "float64"]

    ).columns

    categorical_columns = cleaned_df.select_dtypes(

        include=["object"]

    ).columns

    # Numerical → Fill with median

    for column in numerical_columns:

        cleaned_df[column] = (

            cleaned_df[column].fillna(

                cleaned_df[column].median()
            )
        )

    # Categorical → Fill with mode

    for column in categorical_columns:

        if not cleaned_df[column].mode().empty:

            cleaned_df[column] = (

                cleaned_df[column].fillna(

                    cleaned_df[column].mode()[0]
                )
            )

    return cleaned_df


def remove_duplicate_rows(df):

    cleaned_df = df.copy()

    duplicates_removed = (

        cleaned_df.duplicated().sum()
    )

    cleaned_df = (

        cleaned_df.drop_duplicates()
    )

    return cleaned_df, duplicates_removed


import pandas as pd


def fix_datatypes(df):

    cleaned_df = df.copy()

    for column in cleaned_df.columns:

        # Only object columns

        if cleaned_df[column].dtype == "object":

            try:

                # Sample values

                sample_values = (

                    cleaned_df[column]

                    .dropna()

                    .astype(str)

                    .head(5)
                )

                # Try datetime conversion

                converted = pd.to_datetime(

                    sample_values,

                    errors="coerce"
                )

                # If most values converted successfully

                success_ratio = (

                    converted.notna().sum()

                    / len(sample_values)
                )

                if success_ratio >= 0.8:

                    cleaned_df[column] = pd.to_datetime(

                        cleaned_df[column],

                        errors="coerce"
                    )

                    print(
                        f"Converted {column} to datetime"
                    )

            except Exception:

                pass

    return cleaned_df



def handle_outliers(df):

    cleaned_df = df.copy()

    numerical_columns = cleaned_df.select_dtypes(

        include=["int64", "float64"]

    ).columns

    for column in numerical_columns:

        q1 = cleaned_df[column].quantile(0.25)

        q3 = cleaned_df[column].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)

        upper_bound = q3 + (1.5 * iqr)

        cleaned_df[column] = cleaned_df[column].clip(

            lower=lower_bound,

            upper=upper_bound
        )

    return cleaned_df