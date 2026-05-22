from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.tools import tool

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from tools.statistical_tools import (

    get_strong_correlations,

    analyze_variance,

    analyze_covariance,

    analyze_trends,

    perform_regression_analysis,

    analyze_distribution
)


load_dotenv()

GLOBAL_DF = None

from config.settings import Settings
from core.factories.llm_factory import (
    LLMFactory
)

llm = (
    LLMFactory
    .get_tool_calling_llm()
)


@tool
def strong_correlation_tool(dummy: str = ""):

    """
    Identify strong correlations
    between numerical features.
    """

    return get_strong_correlations(
        GLOBAL_DF
    )


@tool
def variance_analysis_tool(dummy: str = ""):

    """
    Analyze variance in numerical columns.
    """

    return analyze_variance(
        GLOBAL_DF
    )


@tool
def covariance_analysis_tool(dummy: str = ""):

    """
    Analyze covariance between numerical features.
    """

    return analyze_covariance(
        GLOBAL_DF
    )


@tool
def trend_analysis_tool(dummy: str = ""):

    """
    Analyze trends using datetime columns.
    """

    return analyze_trends(
        GLOBAL_DF
    )


@tool
def regression_analysis_tool(dummy: str = ""):

    """
    Perform regression analysis on
    numerical features.
    """

    return perform_regression_analysis(
        GLOBAL_DF
    )


@tool
def distribution_analysis_tool(dummy: str = ""):

    """
    Analyze data distribution
    for numerical columns.
    """

    return analyze_distribution(
        GLOBAL_DF
    )


tools = [

    strong_correlation_tool,

    variance_analysis_tool,

    covariance_analysis_tool,

    trend_analysis_tool,

    regression_analysis_tool,

    distribution_analysis_tool
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an intelligent
            Statistical Analysis Agent
            inside an Autonomous
            Data Analytics Platform.

            Your responsibility is to
            intelligently analyze the dataset
            and dynamically decide which
            statistical tools should be used.

            IMPORTANT INSTRUCTIONS:

            - Use available statistical tools
              wisely based on the type of data
              present in the dataset.

            - Analyze dataset metadata before
              selecting tools.

            - Use correlation analysis only
              when multiple numerical columns
              are available.

            - Use variance and covariance
              analysis only for meaningful
              numerical data.

            - Use regression analysis only
              if relationships between numerical
              features can be analyzed.

            - Use trend analysis only when
              datetime columns exist.

            - Use distribution analysis only
              for numerical columns.

            - Avoid unnecessary tool calls.

            - Do not call every tool blindly.

            - Select only the most relevant
              tools for the given dataset.

            - Perform efficient and meaningful
              statistical analysis.

            - Return structured and useful
              analytical insights.
            """
        ),

        ("human", "{input}"),

        ("placeholder", "{agent_scratchpad}")
    ]
)

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

def statistical_analysis_agent(state):

    global GLOBAL_DF

    try:

        df = state["dataframe"]

        GLOBAL_DF = df

        dataset_info = {

            "columns":
            list(df.columns),

            "dtypes":
            df.dtypes.astype(str).to_dict(),

            "shape":
            df.shape,

            "eda_results":
            state["eda_results"]

            .get(
                "structured_data",
                {}
            )
        }

        result = agent_executor.invoke(
            {
                "input":
                f"""
                Perform statistical analysis
                on this dataset.

                Dataset Metadata:

                {dataset_info}
                """
            }
        )

        state["statistical_results"] = {

            "structured_data":
            result,

            "statistical_report":
            result["output"]
        }

        state["current_agent"] = (
            "statistical_analysis_agent"
        )

        return state

    except Exception as e:

        print(
            "\nStatistical Agent Error:",
            e
        )

        state["errors"].append(
            str(e)
        )

        return state