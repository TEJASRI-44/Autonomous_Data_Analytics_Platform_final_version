from agents.report_generation_agent import report_generation_agent

sample_state = {
    "dataset_summary":{
        "summary_report":"summary"
    },
    "eda_results":{
        "structured_data":"eda"
    },
    "cleaning_results":{
        "structured_data":"cleaning"
    },
    "statistical_results":{
        "structured_data":"stats"
    },
    "insights":{
        "structured_data":"insights"
    },
    "visualizations":[],
    "final_report":"",
    "report_path":"",
    "workflow_complete":False,
    "current_agent":"",
    "errors":[]
}

def test_report_generation_agent():

    result = report_generation_agent(sample_state)

    assert result["final_report"] != ""
    assert result["report_path"] != ""
    assert result["workflow_complete"] == True
    assert result["current_agent"] == "report_generation_agent"
    assert len(result["errors"]) == 0