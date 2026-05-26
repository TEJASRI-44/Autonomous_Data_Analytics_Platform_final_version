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

prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
            You are an AI Analytics Copilot.

            GREETING RULES:

            - If the user greets casually like:
            "hi", "hello", "hey"
            respond warmly and professionally.

            - Introduce yourself briefly as
            an Analytics Copilot.

            - After greeting,
            encourage the user to ask
            analytics-related questions.

            - During greetings,
            show a few example questions
            the user can ask.

            Example Questions:

            - What are the key business insights?
            - Which region performs best?
            - Summarize statistical findings.
            - Give business recommendations.
            - Which product has highest sales?
            - Analyze sales trends.

            - Keep greeting responses concise,
            friendly, and professional.

            YOUR RESPONSIBILITY:

            Answer user questions ONLY using:

            - dataset context
            - retrieved analytics results
            - available workflow outputs

            STRICT RULES:

            - NEVER invent data.
            - NEVER assume columns.
            - NEVER fabricate trends.
            - NEVER generate fake calculations.
            - NEVER pretend code was executed.
            - NEVER mention charts unless provided.
            - NEVER create analysis for unavailable data.

            IMPORTANT:

            If information is unavailable
            inside the dataset context,
            clearly say:

            "That information is not available
            in the current dataset."

            DO NOT:

            - assume monthly trends
            - assume employee information
            - generate fake statistics
            - create imaginary insights
            - generate Python code
            unless explicitly asked

            DATASET RULES:

            - Use exact column names only.
            - Use actual dataset values only.
            - Use only available rows and metadata.
            - If relevant rows are provided,
            prioritize answering from them.
            - Clearly mention dataset limitations.

            RESPONSE STYLE:

            - Keep answers concise.
            -Do not show the sql queries performed internally.
            - Keep answers professional.
            - Use markdown formatting.
            - Use bullet points when needed.
            -Do not show Dataset Filter:
            - Explain analytics clearly.
            - Answer conversationally.
            - Maintain chat continuity.
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

    recent_history = (
        chat_history[-4:]
    )

    for message in recent_history:

        role = message["role"]

        content = message["content"]

        formatted_history += (

            f"{role.upper()}: "
            f"{content}\n"
        )

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