from agents.data_ingestion_agent import (
    data_ingestion_agent
)

from agents.eda_agent import (
    eda_agent
)


initial_state = {

    "file_path":
    "sample_data/sales_data.csv",

    "dataframe": None,

    "dataset_summary": {},

    "eda_results": {},

    "statistical_results": {},

    "visualizations": [],

    "insights": "",

    "final_report": "",

    "current_agent": "",

    "errors": []
}


def get_eda_result():

    ingestion_result = (
        data_ingestion_agent(initial_state)
    )

    result = eda_agent(
        ingestion_result
    )

    return result


def test_eda_results_generated():

    result = get_eda_result()

    assert len(
        result["eda_results"]
    ) > 0


def test_numerical_columns_detected():

    result = get_eda_result()

    assert len(

        result["eda_results"]
        ["numerical_columns"]

    ) > 0


def test_categorical_columns_detected():

    result = get_eda_result()

    assert len(

        result["eda_results"]
        ["categorical_columns"]

    ) > 0


def test_summary_statistics_generated():

    result = get_eda_result()

    assert (

        "summary_statistics"

        in result["eda_results"]

    )


def test_correlation_matrix_generated():

    result = get_eda_result()

    assert (

        "correlation_matrix"

        in result["eda_results"]

    )


def test_missing_values_generated():

    result = get_eda_result()

    assert (

        "missing_values"

        in result["eda_results"]

    )


def test_outliers_generated():

    result = get_eda_result()

    assert (

        "outliers"

        in result["eda_results"]

    )


def test_memory_usage_generated():

    result = get_eda_result()

    assert (

        "memory_usage"

        in result["eda_results"]

    )


def test_duplicate_rows_generated():

    result = get_eda_result()

    assert (

        "duplicate_rows"

        in result["eda_results"]

    )


def test_skewness_generated():

    result = get_eda_result()

    assert (

        "skewness"

        in result["eda_results"]

    )


def test_current_agent_updated():

    result = get_eda_result()

    assert (

        result["current_agent"]

        == "eda_agent"

    )


def test_no_errors():

    result = get_eda_result()

    assert len(
        result["errors"]
    ) == 0