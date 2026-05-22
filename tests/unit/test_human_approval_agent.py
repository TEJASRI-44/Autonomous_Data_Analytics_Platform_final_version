from agents.human_approval_agent import human_approval_agent

def test_human_approval_agent():

    state = {
        "current_agent":"",
        "errors":[]
    }

    result = human_approval_agent(state)

    assert result["current_agent"] == "human_approval_agent"