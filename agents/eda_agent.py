from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq

from langchain_core.tools import tool

from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)
from core.utils.agent_executor_factory import (

    invoke_agent_with_fallback
)

from tools.eda_tools import (

    get_numerical_columns,

    get_categorical_columns,

    get_datetime_columns,

    get_boolean_columns,

    get_dataset_shape,

    analyze_missing_values,

    analyze_missing_percentage,

    detect_duplicate_rows,

    generate_summary_statistics,

    generate_correlation_matrix,

    analyze_unique_values,

    detect_high_cardinality_columns,

    detect_constant_columns,

    analyze_skewness,

    detect_outliers,

    analyze_memory_usage
)


load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

GLOBAL_DF = None
from config.settings import Settings



@tool
def dataset_shape_tool(dummy: str = ""):

    """
    Get dataset rows and columns count.
    """

    return get_dataset_shape(GLOBAL_DF)


@tool
def numerical_columns_tool(dummy: str = ""):

    """
    Identify numerical columns.
    """

    return get_numerical_columns(GLOBAL_DF)


@tool
def categorical_columns_tool(dummy: str = ""):

    """
    Identify categorical columns.
    """

    return get_categorical_columns(GLOBAL_DF)


@tool
def datetime_columns_tool(dummy: str = ""):

    """
    Identify datetime columns.
    """

    return get_datetime_columns(GLOBAL_DF)


@tool
def boolean_columns_tool(dummy: str = ""):

    """
    Identify boolean columns.
    """

    return get_boolean_columns(GLOBAL_DF)


@tool
def missing_values_tool(dummy: str = ""):

    """
    Analyze missing values.
    """

    return analyze_missing_values(GLOBAL_DF)


@tool
def missing_percentage_tool(dummy: str = ""):

    """
    Analyze missing value percentages.
    """

    return analyze_missing_percentage(GLOBAL_DF)


@tool
def duplicate_rows_tool(dummy: str = ""):

    """
    Detect duplicate rows.
    """

    return detect_duplicate_rows(GLOBAL_DF)


@tool
def summary_statistics_tool(dummy: str = ""):

    """
    Generate summary statistics.
    """

    return generate_summary_statistics(GLOBAL_DF)


@tool
def correlation_matrix_tool(dummy: str = ""):

    """
    Generate correlation matrix for numerical columns.
    """

    return generate_correlation_matrix(GLOBAL_DF)


@tool
def unique_values_tool(dummy: str = ""):

    """
    Analyze unique values.
    """

    return analyze_unique_values(GLOBAL_DF)


@tool
def high_cardinality_tool(dummy: str = ""):

    """
    Detect high-cardinality columns.
    """

    return detect_high_cardinality_columns(GLOBAL_DF)


@tool
def constant_columns_tool(dummy: str = ""):

    """
    Detect constant columns.
    """

    return detect_constant_columns(GLOBAL_DF)


@tool
def skewness_tool(dummy: str = ""):

    """
    Analyze skewness in numerical columns.
    """

    return analyze_skewness(GLOBAL_DF)


@tool
def outlier_detection_tool(dummy: str = ""):

    """
    Detect outliers in numerical columns.
    """

    return detect_outliers(GLOBAL_DF)


@tool
def memory_usage_tool(dummy: str = ""):

    """
    Analyze dataframe memory usage.
    """

    return analyze_memory_usage(GLOBAL_DF)

tools = [
    dataset_shape_tool,
    numerical_columns_tool,
    categorical_columns_tool,
    datetime_columns_tool,
    boolean_columns_tool,
    missing_values_tool,
    missing_percentage_tool,
    duplicate_rows_tool,
    summary_statistics_tool,
    correlation_matrix_tool,
    unique_values_tool,
    high_cardinality_tool,
    constant_columns_tool,
    skewness_tool,
    outlier_detection_tool,
    memory_usage_tool
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an intelligent
            Exploratory Data Analysis (EDA) Agent
            inside an Autonomous Data Analytics Platform.

            Your responsibility is to explore,
            understand,
and analyze the dataset structure
            and quality.

            IMPORTANT RESPONSIBILITIES:

            - Understand dataset structure.
            - Identify numerical, categorical,
              datetime, and boolean columns.
            - Analyze dataset dimensions.
            - Detect missing values and
              missing value percentages.
            - Detect duplicate rows.
            - Generate summary statistics.
            - Analyze correlations between
              numerical features.
            - Detect high-cardinality columns.
            - Detect constant-value columns.
            - Analyze skewness in numerical data.
            - Detect potential outliers.
            - Analyze dataframe memory usage.

            TOOL USAGE INSTRUCTIONS:

            - Use tools dynamically based on
              dataset characteristics.
            - Do not call every tool blindly.
            - Avoid unnecessary analysis.
            - Select only relevant tools
              for the current dataset.
            - Use correlation analysis only
              if multiple numerical colum
            IMPORTANT CONSTRAINTS:

            - Do NOT clean or modify the dataset.
            - Do NOT remove missing values.
            - Do NOT remove duplicates.
            - Do NOT transform columns.
            - Do NOT perform feature engineering.
ns exist.
            - Use skewness and outlier analysis
              only for meaningful numerical columns.
            - Use datetime analysis only if
              datetime columns exist.

            IMPORTANT CONSTRAINTS:

            - Do NOT clean or modify the dataset.
            - Do NOT remove missing values.
            - Do NOT remove duplicates.
            - Do NOT transform columns.
            - Do NOT perform feature engineering.

            Your role is ONLY to:
            analyze,
            inspect,
            and understand the dataset.

            Return structured EDA findings
            and observations.
            """
        ),

        ("human", "{input}"),

        MessagesPlaceholder(
            variable_name="agent_scratchpad"
        )
    ]
)




def eda_agent(state):

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
            df.shape
        }

        result = invoke_agent_with_fallback(

            tools=tools,

            prompt=prompt,

            input_data={
                "input":
                f"""
                Perform exploratory data analysis
                on this dataset.

                Dataset Metadata:

                {dataset_info}
                """
            }
        )
        dataset_shape = get_dataset_shape(df)

        numerical_columns = get_numerical_columns(df)

        categorical_columns = get_categorical_columns(df)

        datetime_columns = get_datetime_columns(df)

        missing_values = analyze_missing_values(df)

        duplicate_rows = detect_duplicate_rows(df)

        summary_statistics = generate_summary_statistics(df)

        correlation_matrix = generate_correlation_matrix(df)
        state["eda_results"] = {

            "structured_data": {

                "dataset_shape":
                dataset_shape,

                "numerical_columns":
                numerical_columns,

                "categorical_columns":
                categorical_columns,

                "datetime_columns":
                datetime_columns,

                "missing_values":
                missing_values,

                "duplicate_rows":
                duplicate_rows,

                "summary_statistics":
                summary_statistics,

                "correlation_matrix":
                correlation_matrix
            },

            "eda_report":
            result["output"]
        }
        state["current_agent"] = (
            "eda_agent"
        )

        return state

    except Exception as e:

        print("\nEDA Agent Error:", e)

        state["errors"].append(str(e))

        return state