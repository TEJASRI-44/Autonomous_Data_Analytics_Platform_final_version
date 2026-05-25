from langchain_groq import (
    ChatGroq
)

from langchain.agents import (

    AgentExecutor,

    create_tool_calling_agent
)

from config.settings import (
    Settings
)


def invoke_agent_with_fallback(

    tools,

    prompt,

    input_data
):

    models = [

        Settings.TOOL_CALLING_MODEL,

        *Settings.FALLBACK_TOOL_MODELS
    ]

    last_exception = None

    for model_name in models:

        try:

            print(
                f"\nTrying Model: {model_name}"
            )

            llm = ChatGroq(

                model=model_name,

                temperature=(
                    Settings.TEMPERATURE
                )
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

            result = agent_executor.invoke(
                input_data
            )

            print(
                f"\nUsing Model: {model_name}"
            )

            return result

        except Exception as e:

            print(
                f"\nModel Failed: {model_name}"
            )

            print(e)

            last_exception = e

    raise Exception(

        f"All models failed: {last_exception}"
    )