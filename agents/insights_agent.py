from dotenv import load_dotenv

from langchain_core.prompts import (
    ChatPromptTemplate
)

load_dotenv()

from core.factories.llm_factory import (
    LLMFactory
)

from core.utils.llm_utils import (
    clean_llm_output
)

llm = (
    LLMFactory
    .get_tool_calling_llm()
)

prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
            You are an expert
            Data Insights Analyst
            inside an Autonomous
            Data Analytics Platform.

            Your responsibilities:

            - Generate business insights
            - Identify key trends
            - Detect anomalies
            - Analyze statistical findings
            - Interpret visualizations
            - Generate recommendations
            - Highlight risks and opportunities

            IMPORTANT INSTRUCTIONS:

            - Focus on meaningful insights.
            - Avoid generic statements.
            - Generate actionable observations.
            - Keep insights professional,
              concise,
              and business-friendly.

            Focus on:
            correlations,
            trends,
            anomalies,
            distributions,
            and business impact.
            """
        ),

        ("human", "{input}")
    ]
)

chain = prompt | llm


def insights_agent(state):

    try:

        print(
            "\n[Insights Agent Started]"
        )

        # EDA RESULTS

        eda_results = (

            state["eda_results"]

            .get(
                "structured_data",
                {}
            )
        )

        # STATISTICAL RESULTS
        statistical_results = (

            state["statistical_results"]

            .get(
                "structured_data",
                {}
            )
        )

        visualizations = (
            state.get(
                "visualizations",
                []
            )
        )

        visualization_summaries = []

        for visualization in visualizations:

            visualization_summaries.append(

                {
                    "title":
                    visualization.get(
                        "title",
                        ""
                    )
                }
            )

        human_feedback = (
            state.get(
                "human_feedback",
                ""
            )
        )
        insights_input = f"""

        EDA RESULTS:
        {eda_results}

        STATISTICAL RESULTS:
        {statistical_results}

        GENERATED VISUALIZATIONS:
        {visualization_summaries}

        HUMAN FEEDBACK:
        {human_feedback}

        IMPORTANT:
        If human feedback is present,
        carefully analyze the feedback
        and prioritize generating
        improved insights based on it.

        Generate:

        - Business insights
        - Trend analysis
        - Anomaly observations
        - Recommendations
        - Statistical interpretations
        """


        result = chain.invoke(

            {

                "input":
                insights_input
            }
        )

        cleaned_results = (
            clean_llm_output(
                result.content
            )
        )

        insights = cleaned_results


        state["insights"] = {

            "insights_report":
            insights
        }

        state["current_agent"] = (
            "insights_agent"
        )

        print(
            "\nInsights Generated"
        )

        return state

    except Exception as e:

        print(
            "\nInsights Agent Error:",
            e
        )

        state["insights"] = {

            "insights_report":
            (
                "Insights Generation Failed:\n"
                f"{str(e)}"
            )
        }

        state["errors"].append(
            str(e)
        )

        return state