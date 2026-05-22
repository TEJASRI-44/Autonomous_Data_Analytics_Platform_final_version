from graph.workflow import graph

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
    "approval_status":"approved",
    "human_feedback":""
}

def test_complete_workflow():

    result = graph.invoke(
        initial_state
    )

    assert result["workflow_complete"] == True
    assert result["final_report"] != ""
    assert result["report_path"] != ""
    assert len(result["errors"]) == 0