def human_approval_agent(state):

    print(
        "\n[Human Approval Agent Running]"
    )

    feedback = state.get(
        "human_feedback",
        ""
    )

    approval_status = state.get(
        "approval_status",
        ""
    )

    previous_insights = (

        state.get(
            "insights",
            {}
        ).get(
            "insights_report",
            ""
        )
    )

    if (
        approval_status
        ==
        "rejected"
    ):

        state[
            "previous_insights"
        ] = previous_insights

    state[
        "current_agent"
    ] = "human_approval_agent"

    return state