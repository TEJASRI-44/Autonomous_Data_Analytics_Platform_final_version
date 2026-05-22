from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

from langchain_core.tools import tool

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from tools.data_cleaning_tools import (

    handle_missing_values,

    remove_duplicate_rows,

    fix_datatypes,

    handle_outliers
)

load_dotenv()

groq_api_key = os.getenv(
    "GROQ_API_KEY"
)



GLOBAL_DF = None


from core.factories.llm_factory import (
    LLMFactory
)


llm = (
    LLMFactory
    .get_tool_calling_llm()
)


@tool
def missing_value_cleaning_tool( columns: list = None,

    dtypes: dict = None):

    """
    Handle missing values in dataset.
    """

    global GLOBAL_DF

    GLOBAL_DF = handle_missing_values(
        GLOBAL_DF
    )

    return "Missing values handled."


@tool
def duplicate_removal_tool( columns: list = None,

    dtypes: dict = None):

    """
    Remove duplicate rows.
    """

    global GLOBAL_DF

    GLOBAL_DF, duplicates_removed = (

        remove_duplicate_rows(
            GLOBAL_DF
        )
    )

    return f"{duplicates_removed} duplicates removed."


@tool
def datatype_fixing_tool(

    columns: list = None,

    dtypes: dict = None
):

    """
    Fix dataframe datatypes.
    """

    global GLOBAL_DF

    GLOBAL_DF = fix_datatypes(
        GLOBAL_DF
    )

    return "Datatypes fixed."


@tool
def outlier_handling_tool( columns: list = None,

    dtypes: dict = None):

    """
    Handle outliers in numerical columns.
    """

    global GLOBAL_DF

    GLOBAL_DF = handle_outliers(
        GLOBAL_DF
    )

    return "Outliers handled."



tools = [

    missing_value_cleaning_tool,

    duplicate_removal_tool,

    datatype_fixing_tool,

    outlier_handling_tool
]


SYSTEM_PROMPT = """
You are an intelligent
Data Cleaning Agent
inside an Autonomous
Data Analytics Platform.

Your responsibility is to
intelligently clean the dataset
based on EDA findings.

IMPORTANT RESPONSIBILITIES:

- Analyze EDA results carefully.
- Decide which cleaning tools
  should be applied.
- Apply only necessary cleaning steps.
- Avoid unnecessary modifications.

AVAILABLE CLEANING OPERATIONS:

- Handle missing values
- Remove duplicate rows
- Fix datatypes
- Handle outliers

IMPORTANT INSTRUCTIONS:

- Do not call every tool blindly.
- Use missing value cleaning
  only if missing values exist.
- Remove duplicates only if
  duplicates are present.
- Handle outliers only if
  outliers are detected.
- Fix datatypes only if
  datatype inconsistencies exist.

Your goal is to produce a
cleaner and analysis-ready dataset.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT
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


def data_cleaning_agent(state):

    global GLOBAL_DF

    try:

        print(
            "\n[Data Cleaning Agent Started]"
        )

        GLOBAL_DF = state["dataframe"]

        eda_results = (
            state["eda_results"]

            .get(
                "structured_data",
                {}
            )
        )

        result = agent_executor.invoke(
            {
                "input":
                f"""
                Clean this dataset
                intelligently using
                the EDA findings.

                EDA RESULTS:

                {eda_results}
                """
            }
        )


        state["dataframe"] = (
            GLOBAL_DF
        )
        state["cleaning_results"] = {

            "structured_data":
            result,

            "cleaning_report":
            result["output"]
        }

        state["current_agent"] = (
            "data_cleaning_agent"
        )

        print(
            "\nData Cleaning Completed"
        )

        return state

    except Exception as e:

        print(
            "\nCleaning Agent Error:",
            e
        )

        state["errors"].append(
            str(e)
        )

        return state