from agents.insights_agent import insights_agent

def test_insights_agent():

    state = {
        "eda_results":{
            "structured_data":{}
        },
        "statistical_results":{
            "structured_data":{}
        },
        "visualizations":[],
        "human_feedback":"",
        "insights":{},
        "errors":[]
    }

    result = insights_agent(state)

    assert "insights_report" in result["insights"]
    assert result["current_agent"] == "insights_agent"
    assert len(result["errors"]) == 0