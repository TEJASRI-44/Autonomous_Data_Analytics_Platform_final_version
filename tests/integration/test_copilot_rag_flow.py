from agents.copilot_agent import copilot_agent

def test_copilot_rag_flow():

    user_query = "Give business insights"

    chat_history = []

    result = copilot_agent(
        user_query,
        chat_history
    )

    assert result != ""