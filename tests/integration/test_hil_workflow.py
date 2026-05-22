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
    "approval_status":"rejected",
    "human_feedback":"Add more recommendations"
}

def test_hil_workflow():

    result = graph.invoke(
        initial_state
    )

    assert "insights_report" in result["insights"]
    assert len(result["errors"]) == 0