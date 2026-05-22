from agents.data_ingestion_agent import (
    data_ingestion_agent
)


sample_state = {

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


def test_dataset_loaded():

    result = data_ingestion_agent(
        sample_state
    )

    assert result["dataframe"] is not None


def test_dataset_summary_created():

    result = data_ingestion_agent(
        sample_state
    )

    assert (
        "rows"
        in result["dataset_summary"]
    )


def test_column_names_generated():

    result = data_ingestion_agent(
        sample_state
    )

    assert (
        "column_names"
        in result["dataset_summary"]
    )


def test_missing_values_generated():

    result = data_ingestion_agent(
        sample_state
    )

    assert (
        "missing_values"
        in result["dataset_summary"]
    )


def test_current_agent_updated():

    result = data_ingestion_agent(
        sample_state
    )

    assert (
        result["current_agent"]
        == "data_ingestion_agent"
    )


def test_invalid_file():

    invalid_state = sample_state.copy()

    invalid_state["file_path"] = (
        "invalid.csv"
    )

    result = data_ingestion_agent(
        invalid_state
    )

    assert len(result["errors"]) > 0