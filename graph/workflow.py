from langgraph.graph import ( # type: ignore
    StateGraph,
    END
)

from graph.state import AnalyticsState

# Supervisor

from agents.supervisor_agent import (

    supervisor_agent,

    supervisor_router
)

# Agents

from agents.data_ingestion_agent import (
    data_ingestion_agent
)

from agents.eda_agent import (
    eda_agent
)
from agents.data_cleaning_agent import (
    data_cleaning_agent
)

from agents.statistical_analysis_agent import (
    statistical_analysis_agent
)

from agents.visualization_agent import(
    visualization_agent
)
from agents.insights_agent import (
    insights_agent
)
from agents.human_approval_agent import (
    human_approval_agent
)
from agents.report_generation_agent import (
    report_generation_agent
)
# Create workflow

workflow = StateGraph(
    AnalyticsState
)

# -----------------------------
# Add Nodes
# -----------------------------

workflow.add_node(
    "supervisor_agent",
    supervisor_agent
)

workflow.add_node(
    "data_ingestion_agent",
    data_ingestion_agent
)

workflow.add_node(
    "eda_agent",
    eda_agent
)
workflow.add_node(
    "data_cleaning_agent",
    data_cleaning_agent
)
workflow.add_node(
    "statistical_analysis_agent",
    statistical_analysis_agent
)

workflow.add_node(
    "visualization_agent",
    visualization_agent
)
workflow.add_node(
    "insights_agent",
    insights_agent
)
workflow.add_node(
    "human_approval_agent",
    human_approval_agent
)
workflow.add_node(
    "report_generation_agent",
    report_generation_agent
)
# -----------------------------
# Set Entry Point
# -----------------------------

workflow.set_entry_point(
    "supervisor_agent"
)

# -----------------------------
# Supervisor Routing
# -----------------------------

workflow.add_conditional_edges(

    "supervisor_agent",

    supervisor_router,

    {

        "data_ingestion_agent":
        "data_ingestion_agent",

        "eda_agent":
        "eda_agent",
        
        "data_cleaning_agent":
        "data_cleaning_agent",

        "statistical_analysis_agent":
        "statistical_analysis_agent",

        "visualization_agent":
        "visualization_agent",
        
        "insights_agent":
        "insights_agent",
        
        "human_approval_agent":
        "human_approval_agent",
        
        "report_generation_agent":
        "report_generation_agent",

        "end": END
    }
)


workflow.add_edge(
    "data_ingestion_agent",
    "supervisor_agent"
)

workflow.add_edge(
    "eda_agent",
    "supervisor_agent"
)
workflow.add_edge(

    "data_cleaning_agent",

    "supervisor_agent"
)

workflow.add_edge(
    "statistical_analysis_agent",
    "supervisor_agent"
)

workflow.add_edge(
    "visualization_agent",
    "supervisor_agent"
)
workflow.add_edge(
    "insights_agent",
    "supervisor_agent"
)


workflow.add_edge(
    "report_generation_agent",
    "supervisor_agent"
)
graph = workflow.compile()
