import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st

from services.analytics_service import (
    AnalyticsService
)
from services.retriever_service import (
    RetrieverService
)

from config.settings import (
    Settings
)
from agents.copilot_agent import (
    copilot_agent
)

if "workflow_completed" not in st.session_state:
    st.session_state["workflow_completed"] = False

if "workflow_result" not in st.session_state:
    st.session_state["workflow_result"] = None

if "report_path" not in st.session_state:
    st.session_state["report_path"] = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

from config.settings import Settings
from core.factories.llm_factory import (
    LLMFactory
)

llm = (
    LLMFactory
    .get_tool_calling_llm()
)

st.set_page_config(
    page_title=(
        "Autonomous Data Analytics Platform"
    ),
    layout="wide"
)

st.title(
    "Autonomous Data Analytics Platform"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Analyse Dataset",
        "Analytics Chat"
    ]
)


if page == "Analyse Dataset":

    st.subheader(
        "Multi-Agent Analytics Workflow"
    )

    uploaded_file = st.file_uploader(
        "Upload Dataset",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:

        file_path = (
            Settings.UPLOAD_DIR
            / uploaded_file.name
        )

        with open(
            str(file_path),
            "wb"
        ) as file:
            file.write(
                uploaded_file.getbuffer()
            )

        st.success(
            f"File Uploaded Successfully: "
            f"{uploaded_file.name}"
        )

        run_workflow = st.button(
            "Run Analytics Workflow"
        )

        if run_workflow:

            st.session_state[
                "workflow_result"
            ] = None

            st.session_state[
                "workflow_completed"
            ] = False

            st.session_state[
                "report_path"
            ] = ""

            st.session_state[
                "run_workflow"
            ] = True
        # HANDLE INSIGHTS REGENERATION
        # When approval_status is "" and insights is {}
        # it means regenerate was clicked — run only
        # insights portion of the workflow then rerun.
    

        result = st.session_state.get(
            "workflow_result"
        )

        # PERSISTENT RESULT RENDERING
        # Render all previous sections from session state
        # so they stay visible across reruns.

        if result is not None:

            # Dataset Summary
            dataset_summary = result.get(
                "dataset_summary", {}
            )
            if dataset_summary:
                st.expander(
                    "Dataset Summary",
                    expanded=True
                ).markdown(
                    dataset_summary.get(
                        "summary_report",
                        "No Dataset Summary Generated"
                    )
                )

            # EDA Results
            eda_results = result.get(
                "eda_results", {}
            )
            if eda_results:
                st.expander(
                    "EDA Results",
                    expanded=False
                ).write(
                    eda_results.get(
                        "eda_report",
                        "No EDA Report Generated"
                    )
                )

            # Cleaning Results
            cleaning_results = result.get(
                "cleaning_results", {}
            )
            if cleaning_results:
                st.expander(
                    "Cleaning Results",
                    expanded=False
                ).markdown(
                    cleaning_results.get(
                        "cleaning_report",
                        "No Cleaning Report Generated"
                    )
                )

            # Statistical Results
            statistical_results = result.get(
                "statistical_results", {}
            )
            if statistical_results:
                st.expander(
                    "Statistical Results",
                    expanded=False
                ).markdown(
                    statistical_results.get(
                        "statistical_report",
                        "No Statistical Report Generated"
                    )
                )

            # Visualizations
            visualizations = result.get(
                "visualizations", []
            )
            if visualizations:
                st.header(
                    "Generated Visualizations"
                )
                columns = st.columns(2)
                for (
                    index,
                    visualization
                ) in enumerate(visualizations):

                    figure = (
                        visualization.get(
                            "figure"
                        )
                    )

                    title = (
                        visualization.get(
                            "title",
                            f"Visualization {index + 1}"
                        )
                    )

                    with columns[index % 2]:
                        with st.expander(
                            title,
                            expanded=False
                        ):
                            st.plotly_chart(
                                figure,
                                use_container_width=True
                            )

            # Insights
            insights = result.get(
                "insights", {}
            )
            if insights:
                st.expander(
                    "Business Insights",
                    expanded=True
                ).write(
                    insights.get(
                        "insights_report",
                        "No Insights Generated"
                    )
                    if isinstance(insights, dict)
                    else insights
                )

            # Final Report
            final_report = result.get(
                "final_report", ""
            )
            if final_report:
                st.expander(
                    "Final Analytics Report",
                    expanded=False
                ).write(final_report)

        if st.session_state.get("run_workflow"):

            initial_state = {
                "file_path": str(file_path),
                "dataframe": None,
                "dataset_summary": {},
                "eda_results": {},
                "cleaning_results": {},
                "statistical_results": {},
                "visualizations": [],
                "insights": "",
                "final_report": "",
                "report_path": "",
                "current_agent": "",
                "workflow_complete": False,
                "errors": [],
                "approval_status": "",
                "human_feedback": "",
            }

            status = st.status(
                "Running Multi-Agent Workflow...",
                expanded=True
            )

            dataset_placeholder = st.empty()
            eda_placeholder = st.empty()
            cleaning_placeholder = st.empty()
            stats_placeholder = st.empty()
            insights_placeholder = st.empty()
            report_placeholder = st.empty()
            visualization_section = st.container()
            workflow_logs = st.container()

            final_report_path = ""
            result = None

            with status:

                workflow_state = (
                    st.session_state.get(
                        "workflow_result"
                    )
                )

                if workflow_state is None:
                    workflow_state = initial_state

                for event in (
                    AnalyticsService
                    .stream_workflow(
                        workflow_state
                    )
                ):

                    for (
                        node_name,
                        node_state
                    ) in event.items():

                        result = node_state

                        if (
                            node_name
                            ==
                            "data_ingestion_agent"
                        ):
                            dataset_summary = (
                                node_state.get(
                                    "dataset_summary",
                                    {}
                                )
                            )

                            dataset_placeholder.expander(
                                "Dataset Summary",
                                expanded=True
                            ).markdown(
                                dataset_summary.get(
                                    "summary_report",
                                    "No Dataset Summary Generated"
                                )
                            )

                        if (
                            node_name
                            ==
                            "eda_agent"
                        ):
                            eda_placeholder.expander(
                                "EDA Results",
                                expanded=False
                            ).write(
                                node_state.get(
                                    "eda_results",
                                    {}
                                ).get(
                                    "eda_report",
                                    "No EDA Report Generated"
                                )
                            )

                        if (
                            node_name
                            ==
                            "data_cleaning_agent"
                        ):
                            cleaning_results = (
                                node_state.get(
                                    "cleaning_results",
                                    {}
                                )
                            )

                            cleaning_placeholder.expander(
                                "Cleaning Results",
                                expanded=False
                            ).markdown(
                                cleaning_results.get(
                                    "cleaning_report",
                                    "No Cleaning Report Generated"
                                )
                            )

                        if (
                            node_name
                            ==
                            "statistical_analysis_agent"
                        ):
                            statistical_results = (
                                node_state.get(
                                    "statistical_results",
                                    {}
                                )
                            )

                            stats_placeholder.expander(
                                "Statistical Results",
                                expanded=False
                            ).markdown(
                                statistical_results.get(
                                    "statistical_report",
                                    "No Statistical Report Generated"
                                )
                            )

                        if (
                            node_name
                            ==
                            "visualization_agent"
                        ):
                            visualizations = (
                                node_state.get(
                                    "visualizations",
                                    []
                                )
                            )

                            if visualizations:
                                with visualization_section:
                                    st.header(
                                        "Generated Visualizations"
                                    )

                                    columns = st.columns(2)
                                    for (
                                        index,
                                        visualization
                                    ) in enumerate(visualizations):

                                        figure = (
                                            visualization.get(
                                                "figure"
                                            )
                                        )

                                        title = (
                                            visualization.get(
                                                "title",
                                                f"Visualization {index + 1}"
                                            )
                                        )

                                        with columns[index % 2]:
                                            with st.expander(
                                                title,
                                                expanded=False
                                            ):
                                                st.plotly_chart(
                                                    figure,
                                                    use_container_width=True
                                                )

                        if (
                            node_name
                            ==
                            "insights_agent"
                        ):
                            insights_placeholder.expander(
                                "Business Insights",
                                expanded=True
                            ).write(
                                node_state.get(
                                    "insights",
                                    {}
                                ).get(
                                    "insights_report",
                                    "No Insights Generated"
                                )
                                if isinstance(
                                    node_state.get("insights", {}),
                                    dict
                                )
                                else node_state.get("insights", "")
                            )

                        if (
                            node_name
                            ==
                            "report_generation_agent"
                        ):
                            final_report_path = (
                                node_state.get(
                                    "report_path"
                                )
                            )

                            report_placeholder.expander(
                                "Final Analytics Report",
                                expanded=False
                            ).write(
                                node_state.get(
                                    "final_report",
                                    ""
                                )
                            )

            if (
                result.get(
                    "approval_status"
                )
                ==
                "approved"
            ):
                st.session_state[
                    "workflow_completed"
                ] = True

            st.session_state["workflow_result"] = result

            st.session_state["report_path"] = (
                final_report_path
            )

            if (
                result.get(
                    "current_agent"
                )
                ==
                "human_approval_agent"
            ):
                status.update(
                    label=(
                        "Waiting For Human Approval"
                    ),
                    state="running"
                )
            else:
                status.update(
                    label=(
                        "Workflow Completed Successfully"
                    ),
                    state="complete"
                )
        # HUMAN-IN-THE-LOOP (HIL) SCREEN
        # Shown whenever current_agent == human_approval_agent
        # and approval is not yet given.
        # Remains on Analyse Dataset page always.


        result = st.session_state.get(
            "workflow_result"
        )

        if (
            result
            and
            result.get(
                "current_agent"
            )
            ==
            "human_approval_agent"
            and
            result.get(
                "approval_status"
            )
            !=
            "approved"
        ):

            st.warning(
                "Review Generated Insights"
            )

            feedback = st.text_input(
                "Need more insights?"
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "Approve Insights"
                ):
                    # PART 2 — APPROVE BUTTON FINAL BEHAVIOR
                    result["approval_status"] = "approved"

                    st.session_state[
                        "workflow_result"
                    ] = result

                    st.rerun()

            with col2:

                if st.button(
                    "Regenerate Insights"
                ):
                    # PART 2 — REGENERATE BUTTON FINAL BEHAVIOR
                    result["approval_status"] = ""

                    result["human_feedback"] = feedback

                    result["insights"] = {}

                    st.session_state[
                        "workflow_result"
                    ] = result

                    st.rerun()


        result = st.session_state.get(
            "workflow_result"
        )

        if (
            result
            and
            result.get(
                "approval_status"
            )
            ==
            "approved"
            and
            not st.session_state.get(
                "workflow_completed"
            )
        ):
            status = st.status(
                "Generating Final Report...",
                expanded=True
            )

            report_placeholder = st.empty()
            final_report_path = ""

            with status:
                for event in (
                    AnalyticsService
                    .stream_workflow(
                        result
                    )
                ):
                    for (
                        node_name,
                        node_state
                    ) in event.items():

                        if (
                            node_name
                            ==
                            "report_generation_agent"
                        ):
                            final_report_path = (
                                node_state.get(
                                    "report_path",
                                    ""
                                )
                            )

                            st.session_state[
                                "report_path"
                            ] = final_report_path

                            st.session_state[
                                "workflow_completed"
                            ] = True

                            st.session_state[
                                "workflow_result"
                            ] = node_state

                            st.session_state[
                                "run_workflow"
                            ] = False

                            report_placeholder.expander(
                                "Final Analytics Report",
                                expanded=False
                            ).write(
                                node_state.get(
                                    "final_report",
                                    ""
                                )
                            )

            status.update(
                label=(
                    "Workflow Completed Successfully"
                ),
                state="complete"
            )

            st.rerun()


        result = st.session_state.get(
            "workflow_result"
        )

        if result is not None:

            st.header(
                "Errors"
            )

            errors = result.get(
                "errors",
                []
            )

            if errors:
                for error in errors:
                    st.error(error)
            else:
                st.success(
                    "No Errors Found"
                )


elif page == "Analytics Chat":

    if st.session_state.get(
        "workflow_completed"
    ):


        report_path = st.session_state.get(
            "report_path"
        )

        if (
            report_path
            and
            os.path.exists(report_path)
        ):

            st.header(
                "Download Final Report"
            )

            with open(
                report_path,
                "rb"
            ) as pdf_file:

                st.download_button(
                    label="Download PDF Report",
                    data=pdf_file,
                    file_name="analytics_report.pdf",
                    mime="application/pdf"
                )


        st.header(
            "Analytics Copilot"
        )

        for message in (
            st.session_state.messages
        ):
            with st.chat_message(
                message["role"]
            ):
                st.markdown(
                    message["content"]
                )

        user_query = st.chat_input(
            "Ask analytics questions..."
        )

        if user_query:


            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": user_query
                }
            )

            with st.chat_message("user"):
                st.markdown(user_query)



            with st.spinner(
                "Copilot Thinking..."
            ):
                assistant_reply = (
                    copilot_agent(
                        user_query,
                        st.session_state.messages
                    )
                )


            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": assistant_reply
                }
            )


            with st.chat_message("assistant"):
                st.markdown(assistant_reply)

    else:

        st.info(
            "Please complete the analytics workflow "
            "on the 'Analyse Dataset' page first."
        )