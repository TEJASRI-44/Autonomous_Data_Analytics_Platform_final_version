import json

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_groq import (
    ChatGroq
)

from config.settings import (
    Settings
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
            You are a query parsing assistant.

            Extract dataframe filtering
            conditions from user query.

            Return ONLY valid JSON.

            Example:

            {{
                "region": "North",
                "product": "Laptop"
            }}

            IMPORTANT:

            - Use only fields explicitly
              mentioned in query.
            - Do not invent fields.
            - Return empty JSON
              if no filters exist.
            - Do not explain anything.
            """
        ),

        ("human", "{input}")
    ]
)

chain = prompt | llm


def extract_filters(user_query):

    result = chain.invoke(

        {
            "input":
            user_query
        }
    )

    try:

        filters = json.loads(
            result.content
        )

        return filters

    except Exception:

        return {}