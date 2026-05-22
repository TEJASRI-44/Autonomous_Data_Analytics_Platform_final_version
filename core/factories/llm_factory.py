from langchain_groq import ChatGroq

from config.settings import (
    Settings
)

class LLMFactory:

    @staticmethod
    def get_tool_calling_llm():

        return ChatGroq(

            model_name=(
                Settings
                .TOOL_CALLING_MODEL
            ),

            temperature=(
                Settings.TEMPERATURE
            )
        )

    @staticmethod
    def get_reasoning_llm():

        return ChatGroq(

            model_name=(
                Settings
                .REASONING_MODEL
            ),

            temperature=(
                Settings.TEMPERATURE
            )
        )