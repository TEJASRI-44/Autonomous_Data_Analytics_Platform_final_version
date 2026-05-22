def get_strong_correlations(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    correlation_matrix = (

        numerical_df.corr()
    )

    strong_correlations = {}

    for column in correlation_matrix.columns:

        for index in correlation_matrix.index:

            correlation = (
                correlation_matrix.loc[index, column]
            )

            if (

                abs(correlation) > 0.7

                and

                index != column

            ):

                key = f"{index} ↔ {column}"

                strong_correlations[key] = round(
                    correlation,
                    2
                )

    return strong_correlations

def analyze_variance(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    variance = (

        numerical_df.var()

    )

    return variance.to_dict()


def analyze_covariance(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    covariance = (

        numerical_df.cov()

    )

    return covariance.to_dict()


def analyze_trends(df):

    trends = {}

    numerical_columns = (

        df.select_dtypes(
            include=["int64", "float64"]
        ).columns

    )

    for column in numerical_columns:

        first_value = df[column].iloc[0]

        last_value = df[column].iloc[-1]

        if last_value > first_value:

            trends[column] = "Increasing"

        elif last_value < first_value:

            trends[column] = "Decreasing"

        else:

            trends[column] = "Stable"

    return trends


from sklearn.linear_model import (
    LinearRegression
)


def perform_regression_analysis(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    columns = list(
        numerical_df.columns
    )

    if len(columns) < 2:

        return {}

    x_column = columns[0]

    y_column = columns[1]

    X = numerical_df[[x_column]]

    y = numerical_df[y_column]

    model = LinearRegression()

    model.fit(X, y)

    score = model.score(X, y)

    result = {

        "input_feature": x_column,

        "target_feature": y_column,

        "regression_score": round(score, 2)
    }

    return result


def analyze_distribution(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    skewness = (

        numerical_df.skew()

    )

    distribution = {}

    for column, value in skewness.items():

        if value > 1:

            distribution[column] = (
                "Highly Positively Skewed"
            )

        elif value < -1:

            distribution[column] = (
                "Highly Negatively Skewed"
            )

        else:

            distribution[column] = (
                "Approximately Normal"
            )

    return distribution

