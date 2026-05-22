from agents.data_ingestion_agent import data_ingestion_agent

sample_state = {
    "file_path":"sample_data/sales_data.csv",
    "dataframe":None,
    "dataset_summary":{},
    "eda_results":{},
    "cleaning_results":{},
    "statistical_results":{},
    "visualizations":[],
    "insights":{},
    "final_report":"",
    "current_agent":"",
    "workflow_complete":False,
    "errors":[],
    "report_path":"",
    "approval_status":"",
    "human_feedback":""
}

def test_data_ingestion_agent():

    result = data_ingestion_agent(sample_state)

    assert result["dataframe"] is not None
    assert "structured_data" in result["dataset_summary"]
    assert "summary_report" in result["dataset_summary"]
    assert result["current_agent"] == "data_ingestion_agent"
    assert len(result["errors"]) == 0

def test_invalid_file():

    invalid_state = sample_state.copy()

    invalid_state["file_path"] = "invalid.csv"

    result = data_ingestion_agent(invalid_state)

    assert len(result["errors"]) > 0