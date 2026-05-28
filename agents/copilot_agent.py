from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_groq import (
    ChatGroq
)

from config.settings import (
    Settings
)

from services.retriever_service import (
    RetrieverService
)

from core.utils.query_parser import (
    extract_filters
)

llm = ChatGroq(

    model=(
        Settings.COPILOT_MODEL
    ),

    temperature=0
)
import plotly.express as px
import streamlit as st


def generate_visualization(
    user_query,
    dataframe
):

    query = user_query.lower()

    numerical_columns = (

        dataframe
        .select_dtypes(
            include=["int64", "float64"]
        )
        .columns
        .tolist()
    )

    categorical_columns = (

        dataframe
        .select_dtypes(
            include=["object"]
        )
        .columns
        .tolist()
    )

    # =========================
    # HISTOGRAM
    # =========================

    if (

        "histogram" in query

        and

        numerical_columns
    ):

        column = numerical_columns[0]

        fig = px.histogram(

            dataframe,

            x=column,

            title=f"Histogram - {column}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =========================
    # BAR CHART
    # =========================

    elif (

        "bar" in query

        and

        categorical_columns
    ):

        column = categorical_columns[0]

        value_counts = (

            dataframe[column]
            .value_counts()
            .reset_index()
        )

        value_counts.columns = [
            column,
            "count"
        ]

        fig = px.bar(

            value_counts,

            x=column,

            y="count",

            title=f"Bar Chart - {column}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =========================
    # SCATTER PLOT
    # =========================

    elif len(numerical_columns) >= 2:

        fig = px.scatter(

            dataframe,

            x=numerical_columns[0],

            y=numerical_columns[1],

            title="Scatter Plot"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",
            """
            You are an AI Analytics Copilot specialized in
            dataset-driven business analytics.

            CORE RESPONSIBILITY
           
            Answer user questions ONLY using:
            - dataset context
            - retrieved analytics context
            - workflow outputs
            - available dataframe rows

            Provide responses that are:
            - accurate
            - grounded
            - concise
            - business-friendly

            GREETING RULES

            If user greets casually:
            - hi
            - hello
            - hey

            Respond warmly and briefly introduce yourself
            as an Analytics Copilot.

            Suggest example questions like:
            - What are the key business insights?
            - Give business recommendations.

            Keep greetings short and professional.

            STRICT RULES

            - NEVER invent data or statistics.
            - NEVER assume unavailable columns or values.
            - NEVER fabricate trends, calculations, or insights.
            - NEVER use external knowledge.
            - NEVER mention charts unless provided.
            - NEVER generate unsupported recommendations.
            - NEVER pretend analysis was executed.

            Use ONLY:
            - provided dataset rows
            - retrieved analytics context
            - workflow outputs

            If information is unavailable, respond:

            "That information is not available
            in the current dataset."

            DATASET RULES

            - Use exact column names and values only.
            - Use only available rows and metadata.
            - Prioritize relevant dataset rows.
            - Perform calculations ONLY using provided data.
            - Do not estimate or extrapolate values.

            ANALYTICAL RULES

            Before answering:
            1. Identify relevant columns.
            2. Identify relevant rows.
            3. Verify calculations carefully.
            4. Ensure response is fully grounded.

            RESPONSE STYLE

            - Keep answers concise and professional.
            - Use markdown formatting.
            - Use headings and bullet points when useful.
            - Use markdown tables for:
            - comparisons
            - rankings
            - aggregations
            - revenue summaries
            - statistical analysis

            FORMATTING RULES

            - Keep tables aligned and readable.
            - Never break numbers across lines.
            - Format currency properly.

            Example:
            $74,000

            - Use comma-separated formatting.
            - Show exact totals and averages only.
            - Provide short business summaries after analysis.

            NEVER SHOW:
            - SQL queries
            - internal reasoning
            - chain-of-thought
            - hidden calculations
            - dataset filters
            - implementation details

            Responses must always be:
            - factually grounded
            - dataset-driven
            - analytically correct
            - well formatted
            - easy to understand
            """
        
        ),

        ("human", "{input}")
    ]
)

chain = prompt | llm


def copilot_agent(

    user_query,

    chat_history,

    dataframe=None
):

    retrieved_context = (

        RetrieverService
        .retrieve_context(
            user_query
        )
    )

    formatted_history = ""

    recent_history = chat_history[-4:]

    if len(chat_history) > 4:

        summary_prompt = f"""

        Summarize the following analytics conversation
        briefly while preserving:

        - important business context
        - analytical discussions
        - user intent
        - previous conclusions

        CHAT HISTORY:

        {chat_history[:-4]}
        """

        summary_response = llm.invoke(
            summary_prompt
        )

        formatted_history += (

            "CONVERSATION SUMMARY:\n"

            f"{summary_response.content}\n\n"
        )

    for message in recent_history:

        role = message["role"]

        content = message["content"]

        formatted_history += (

            f"{role.upper()}:\n"
            f"{content}\n\n"
        )

    print(formatted_history)
    dataset_context = ""

    if dataframe is not None:

        filters = extract_filters(
            user_query
        )

        filtered_df = dataframe.copy()

        for column, value in filters.items():

            if column in dataframe.columns:

                filtered_df = filtered_df[

                    filtered_df[column]
                    .astype(str)
                    .str.lower()
                    ==
                    str(value).lower()
                ]

        dataset_context = f"""

        DATASET SHAPE:
        {dataframe.shape}

        COLUMN NAMES:
        {list(dataframe.columns)}

        DATA TYPES:
        {dataframe.dtypes.to_dict()}

        RELEVANT DATASET ROWS:
        {dataframe.to_string(index=False)} 
        """

    final_input = f"""

    DATASET CONTEXT:

    {dataset_context}

    ANALYTICS CONTEXT:

    {retrieved_context}

    CHAT HISTORY:

    {formatted_history}

    CURRENT USER QUESTION:

    {user_query}
    """

    for chunk in chain.stream(

        {
            "input":
            final_input
        }

    ):

        if hasattr(
            chunk,
            "content"
        ):

            yield chunk.content
            