import pandas as pd
from agents.statistical_analysis_agent import statistical_analysis_agent

def test_statistical_analysis_agent():

    df = pd.DataFrame({
        "sales":[100,200,300],
        "profit":[10,20,30]
    })

    state = {
        "dataframe":df,
        "eda_results":{
            "structured_data":{}
        },
        "statistical_results":{},
        "errors":[]
    }

    result = statistical_analysis_agent(state)

    assert "statistical_report" in result["statistical_results"]
    assert result["current_agent"] == "statistical_analysis_agent"
    assert len(result["errors"]) == 0