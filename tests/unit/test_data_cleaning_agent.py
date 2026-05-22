import pandas as pd

from agents.data_cleaning_agent import (
    data_cleaning_agent
)

def test_data_cleaning_agent():

    df = pd.DataFrame({

        "sales": [100, 200],

        "profit": [10, 20]
    })

    state = {

        "dataframe": df,

        "eda_results": {

            "structured_data": {}
        },

        "cleaning_results": {},

        "errors": []
    }

    result = data_cleaning_agent(
        state
    )

    assert (

        result["current_agent"]

        == "data_cleaning_agent"
    )

    assert (

        "cleaning_report"

        in result["cleaning_results"]
    )

    assert (

        result["dataframe"]

        is not None
    )

    assert len(
        result["errors"]
    ) == 0