from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate
)
from services.report_service import (
            ReportService
)
from services.vector_store_service import (
    VectorStoreService
)
load_dotenv()
from services.vector_store_service import (
    VectorStoreService
)

from config.settings import Settings
from core.factories.llm_factory import (
    LLMFactory
)
from core.utils.llm_utils import clean_llm_output
llm = (
    LLMFactory
    .get_tool_calling_llm()
)


prompt = ChatPromptTemplate.from_messages(

    [

        (

            "system",

            """
            You are an expert
            Report Generation Agent
            inside an Autonomous
            Data Analytics Platform.

            Your responsibility is to
            generate a final professional
            analytics report.

            The report must include:

            1. Dataset Summary
            2. EDA Findings
            3. Data Cleaning Summary
            4. Statistical Findings
            5. Visualization Summary
            6. Business Insights
            7. Recommendations
            8. Final Conclusion

            IMPORTANT INSTRUCTIONS:

            - Keep report professional.
            - Keep report well-structured.
            - Use clear headings.
            - Make report concise but informative.
            - Summarize important findings clearly.
            - Highlight business impact.
            - Include actionable recommendations.

            The final report should look like
            a professional analytics document.
            """
        ),

        ("human", "{input}")
    ]
)


chain = prompt | llm


def report_generation_agent(state):

    try:

        print(
            "\n[Report Generation Agent Started]"
        )

        dataset_summary = (

            state["dataset_summary"]

            .get(
                "summary_report",
                ""
            )
        )

        eda_results = (

            state["eda_results"]

            .get(
                "structured_data",
                ""
            )
        )

        cleaning_results = (

            state["cleaning_results"]

            .get(
                "structured_data",
                ""
            )
        )

        statistical_results = (

            state["statistical_results"]

            .get(
                "structured_data",
                ""
            )
        )

        insights = (

            state["insights"]

            .get(
                "structured_data",
                ""
            )
        )

        visualizations = (
            state["visualizations"]
        )


        report_input = f"""

        DATASET SUMMARY:
        {dataset_summary}

        EDA SUMMARY:
        {str(eda_results)[:1500]}

        CLEANING RESULTS:
        {str(cleaning_results)[:1500]}

        STATISTICAL RESULTS:
        {str(statistical_results)[:1500]}

        BUSINESS INSIGHTS:
        {str(insights)[:2000]}

        VISUALIZATIONS:
        {visualizations[:5]}

        Generate final professional report.
        """

        result = chain.invoke(

            {
                "input":
                report_input
            }
        )
        cleaned_results=clean_llm_output(result.content)
        final_report = cleaned_results

        state["final_report"] = (
            final_report
        )

        report_path = (

            ReportService.save_report(
                final_report
            )
        )

        print(
            "\nGenerated Report Path:",
            report_path
        )

        state["report_path"] = (
            report_path
        )

        VectorStoreService.store_workflow_results(
            state
        )

        state["workflow_complete"] = True

        state["current_agent"] = (
            "report_generation_agent"
        )

        print(
            "\nFinal Report Generated"
        )

        return state

    except Exception as e:

        print(
            "\nReport Generation Error:",
            e
        )

        state["errors"].append(
            str(e)
        )

        state["workflow_complete"] = True

        return state