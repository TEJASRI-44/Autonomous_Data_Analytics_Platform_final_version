def supervisor_agent(state):

    print(
        "\n[Supervisor Agent Running]"
    )

    state["current_agent"] = (
        "supervisor_agent"
    )

    return state


def supervisor_router(state):

    print(
        "\n[Supervisor Routing]"
    )

    if state.get(
        "workflow_complete"
    ):

        print(
            "\nWorkflow Completed"
        )

        return "end"



    if len(

        state.get("errors", [])

    ) >= 3:

        print(
            "\nToo Many Errors."
        )

        state["workflow_complete"] = True

        return "end"



    if state.get("dataframe") is None:

        print(
            "\nRouting → Data Ingestion Agent"
        )

        return (
            "data_ingestion_agent"
        )


    if not state.get(
        "eda_results"
    ):

        print(
            "\nRouting → EDA Agent"
        )

        return "eda_agent"


    if not state.get(
        "cleaning_results"
    ):

        print(
            "\nRouting → Data Cleaning Agent"
        )

        return (
            "data_cleaning_agent"
        )


    if not state.get(
        "statistical_results"
    ):

        print(
            "\nRouting → Statistical Analysis Agent"
        )

        return (
            "statistical_analysis_agent"
        )



    if not state.get(
        "visualizations"
    ):

        print(
            "\nRouting → Visualization Agent"
        )

        return (
            "visualization_agent"
        )



    if not state.get(
        "insights"
    ):

        print(
            "\nRouting → Insights Agent"
        )

        return "insights_agent"



    approval_status = state.get(
        "approval_status",
        ""
    )

    current_agent = state.get(
        "current_agent",
        ""
    )

    if (
        state.get("insights")
        and
        approval_status != "approved"
    ):

        if (
            current_agent
            !=
            "human_approval_agent"
        ):

            print(
                "\nRouting → Human Approval Agent"
            )

            return "human_approval_agent"

        print(
            "\nWaiting For Human Approval"
        )

        state[
            "workflow_complete"
        ] = False

        return "end"


    if (
        state.get(
            "approval_status"
        )
        ==
        "approved"
    ):

        print(
            "\nRouting → Report Generation Agent"
        )

        return (
            "report_generation_agent"
        )

    print(
        "\nWorkflow Successfully Completed"
    )

    state["workflow_complete"] = True

    return "end"