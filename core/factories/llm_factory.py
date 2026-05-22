from langchain_groq import ChatGroq

from config.settings import (
    Settings
)


class LLMFactory:

    @staticmethod
    def get_tool_calling_llm():

        models = [

            Settings.TOOL_CALLING_MODEL,

            *Settings.FALLBACK_TOOL_MODELS
        ]

        for model in models:

            try:

                llm = ChatGroq(

                    model=model,

                    temperature=
                    Settings.TEMPERATURE
                )

                return llm

            except Exception as e:

                print(
                    f"\nModel Failed: {model}"
                )

        raise Exception(
            "All models failed."
        )