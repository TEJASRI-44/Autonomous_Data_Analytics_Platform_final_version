from agents.copilot_agent import copilot_agent

def test_copilot_agent():

    user_query = "Give sales insights"

    chat_history = []

    result = copilot_agent(
        user_query,
        chat_history
    )

    assert result != ""