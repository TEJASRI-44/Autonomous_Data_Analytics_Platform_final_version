from agents.data_ingestion_agent import (
    data_ingestion_agent
)

from agents.statistical_analysis_agent import (
    statistical_analysis_agent
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


def get_statistical_result():

    ingestion_result = (
        data_ingestion_agent(initial_state)
    )

    result = statistical_analysis_agent(
        ingestion_result
    )

    return result


def test_statistical_results_generated():

    result = get_statistical_result()

    assert len(
        result["statistical_results"]
    ) > 0


def test_correlation_analysis_generated():

    result = get_statistical_result()

    assert (

        "strong_correlations"

        in result["statistical_results"]

    )


def test_variance_analysis_generated():

    result = get_statistical_result()

    assert (

        "variance_analysis"

        in result["statistical_results"]

    )


def test_regression_analysis_generated():

    result = get_statistical_result()

    assert (

        "regression_analysis"

        in result["statistical_results"]

    )


def test_trend_analysis_generated():

    result = get_statistical_result()

    assert (

        "trend_analysis"

        in result["statistical_results"]

    )


def test_current_agent_updated():

    result = get_statistical_result()

    assert (

        result["current_agent"]

        == "statistical_analysis_agent"

    )


def test_no_errors():

    result = get_statistical_result()

    assert len(
        result["errors"]
    ) == 0