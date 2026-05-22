from agents.data_ingestion_agent import data_ingestion_agent
from agents.eda_agent import eda_agent

initial_state = {
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

def test_eda_agent():

    ingestion_result = data_ingestion_agent(initial_state)

    result = eda_agent(ingestion_result)

    assert "structured_data" in result["eda_results"]
    assert "dataset_shape" in result["eda_results"]["structured_data"]
    assert "numerical_columns" in result["eda_results"]["structured_data"]
    assert "categorical_columns" in result["eda_results"]["structured_data"]
    assert "datetime_columns" in result["eda_results"]["structured_data"]
    assert "missing_values" in result["eda_results"]["structured_data"]
    assert "duplicate_rows" in result["eda_results"]["structured_data"]
    assert "summary_statistics" in result["eda_results"]["structured_data"]
    assert "correlation_matrix" in result["eda_results"]["structured_data"]
    assert "eda_report" in result["eda_results"]
    assert result["current_agent"] == "eda_agent"
    assert len(result["errors"]) == 0