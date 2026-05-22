import pandas as pd
from agents.visualization_agent import visualization_agent

def test_visualization_agent():

    df = pd.DataFrame({
        "sales":[100,200,300],
        "profit":[10,20,30]
    })

    state = {
        "dataframe":df,
        "eda_results":{
            "structured_data":{
                "numerical_columns":["sales","profit"],
                "categorical_columns":[],
                "datetime_columns":[]
            }
        },
        "visualizations":[],
        "errors":[]
    }

    result = visualization_agent(state)

    assert len(result["visualizations"]) > 0
    assert result["current_agent"] == "visualization_agent"
    assert len(result["errors"]) == 0