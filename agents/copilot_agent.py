from langchain_core.prompts import (
    ChatPromptTemplate
)

from core.factories.llm_factory import (
    LLMFactory
)

from services.retriever_service import (
    RetrieverService
)

llm = (
    LLMFactory
    .get_tool_calling_llm()
)
from core.utils.llm_utils import clean_llm_output

prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
            You are an AI Analytics Copilot.

            Your responsibility is to answer
            user questions based ONLY on
            the analytics workflow results.

            Use the provided analytics context
            carefully.

            IMPORTANT:

            - Answer conversationally.
            - Maintain chat continuity.
            - Use previous conversation context.
            - Keep responses professional.
            - Keep explanations concise.
            - Explain analytics clearly.
            - Avoid hallucinations.
            """
        ),

        ("human", "{input}")
    ]
)

chain = prompt | llm


def copilot_agent(

    user_query,

    chat_history
):



    retrieved_context = (

        RetrieverService
        .retrieve_context(
            user_query
        )
    )


    formatted_history = ""

    for message in chat_history:

        role = message["role"]

        content = message["content"]

        formatted_history += (

            f"{role.upper()}: "
            f"{content}\n"
        )


    final_input = f"""

    ANALYTICS CONTEXT:

    {retrieved_context}

    CHAT HISTORY:

    {formatted_history}

    CURRENT USER QUESTION:

    {user_query}
    """

    result = chain.invoke(

        {
            "input":
            final_input
        }
    )
    cleaned_results=clean_llm_output(result.content)
    return cleaned_results