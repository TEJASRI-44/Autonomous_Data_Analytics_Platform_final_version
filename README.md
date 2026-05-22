# Autonomous Data Analytics Platform with Analytics Copilot

## Project Overview

Autonomous Data Analytics Platform is a multi-agent AI system that automates end-to-end data analysis workflows using LangGraph and LangChain.

The platform accepts structured datasets, performs automated analytics through specialized agents, generates interactive visualizations, extracts business insights, creates final analytics reports, and stores workflow knowledge in a vector database for retrieval-based analytics copilot interactions.

The system includes:

- Multi-agent orchestration
- Human-in-the-loop insight review
- Persistent vector memory
- Interactive analytics copilot
- Streamlit dashboard UI
- Dynamic Plotly visualizations

---

# Features

## Multi-Agent Workflow

The workflow is orchestrated using LangGraph with dedicated agents for:

- Data ingestion
- Exploratory Data Analysis (EDA)
- Data cleaning
- Statistical analysis
- Visualization generation
- Business insight generation
- Human approval workflow
- Final report generation
- Analytics copilot interaction

### Implemented Agents

- Supervisor Agent
- Data Ingestion Agent
- EDA Agent
- Data Cleaning Agent
- Statistical Analysis Agent
- Visualization Agent
- Insights Agent
- Human Approval Agent (HIL)
- Report Generation Agent
- Analytics Copilot Agent

---

## Autonomous Analytics Pipeline

The platform automatically:

- Loads datasets
- Detects data types
- Performs EDA
- Cleans missing and duplicate values
- Generates statistical summaries
- Creates visualizations
- Produces business insights
- Generates final analytics reports

---

## Human-in-the-Loop (HIL) Insight Review

Before final report generation:

- Generated insights are shown to the user
- User can approve insights
- User can request additional insights
- Human feedback is appended to the insights prompt
- Insights are regenerated iteratively
- Workflow supports pause/resume handling
- Streamlit session state preserves UI flow

---

## Interactive Visualizations

Dynamic Plotly visualizations include:

- Correlation heatmaps
- Histograms
- Boxplots
- Scatter plots
- Line charts
- Bar charts
- Trend analysis charts

Visualizations are generated dynamically based on dataset schema and rendered inside Streamlit containers.

---

## Analytics Copilot (RAG-Based)

The platform includes a conversational analytics copilot.

### Features

- Answers questions about analyzed datasets
- Uses retrieval from ChromaDB vector database
- Maintains conversational history
- Supports analytics-focused Q&A
- Retrieves workflow-generated context

### RAG Architecture Components

- ChromaDB
- HuggingFace Embeddings
- LangChain Retrieval
- Retriever Service
- Embedding Factory
- Vector Store Service

---

## PDF Report Generation

The platform generates downloadable analytics reports containing:

- Dataset overview
- EDA findings
- Cleaning summary
- Statistical findings
- Visualization summary
- Business insights
- Recommendations
- Final conclusions

---

# Workflow Architecture

```text
Dataset Upload
      ↓
Data Ingestion
      ↓
EDA Analysis
      ↓
Data Cleaning
      ↓
Statistical Analysis
      ↓
Visualization Generation
      ↓
Business Insights Generation
      ↓
Human Approval / Regeneration
      ↓
Report Generation
      ↓
Vector Database Storage
      ↓
Analytics Copilot
```

---

# Project Structure

```text
autonomous-data-analytics-platform/
│
├── agents/
│   ├── supervisor_agent.py
│   ├── data_ingestion_agent.py
│   ├── eda_agent.py
│   ├── data_cleaning_agent.py
│   ├── statistical_analysis_agent.py
│   ├── visualization_agent.py
│   ├── insights_agent.py
    ├── human_in_the_loop_agent.py
    ├── copilot_agent.py
│   ├── report_generation_agent.py
│   └── analytics_copilot_agent.py
│
├── app/
│   └── streamlit_app.py
│
├── config/
│   └── settings.py
│
├── core/
│   └── factories/
│       ├── llm_factory.py
│       └── embedding_factory.py
│
├── graph/
│   ├── state.py
│   └── workflow.py
│
├── repositories/
│   └── analytics_repository.py
    └── report_repository.py
    └── vector_repository.py
│
├── services/
│   ├── analytics_service.py
│   ├── report_service.py
│   ├── retriever_service.py
│   ├── vector_store_service.py
│   ├── storage_service.py
│   └── insight_review_service.py
│
├── tools/
│   └── visualization_tools.py
    └── data_ingestion_tools.py
    └── eda_tools.py
    └── data_cleaning_tools.py
    └── statistical_tools.py
│
├── reports/
│   └── final_report.pdf
│
├── vectordb/
│
├── requirements.txt
│
└── README.md
```

---

# UI Structure

## 1. Analyse Dataset Page

Contains:

- Dataset upload
- Workflow execution
- EDA results
- Cleaning results
- Statistical analysis
- Visualizations
- Insight generation
- Human approval workflow
- Report generation

## 2. Analytics Chat Page

Contains:

- Analytics Copilot
- Conversational analytics Q&A
- Chat history
- Generated report interaction

---

# Installation

## Recommended Python Version

Use Python 3.11.

Python 3.13 is not recommended because some dependencies are incompatible.

---

## Clone Repository

```bash
git clone <repository-url>
cd autonomous-data-analytics-platform
```

---

# Conda Environment Setup

## Create Conda Environment

```bash
conda create -n analytics python=3.11 -y
```

---

## Activate Environment

```bash
conda activate analytics
```

---

## Upgrade pip

```bash
pip install --upgrade pip
```

---

## Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
```

---

# Running the Project

## Start Streamlit Application

```bash
python -m streamlit run app/streamlit_app.py
```

---

# Usage

## Analytics Workflow

1. Upload a CSV dataset
2. Execute analytics workflow
3. Review generated insights
4. Approve or regenerate insights
5. Generate final report
6. Download PDF report
7. Use Analytics Copilot for dataset-related questions

---

## Example Copilot Questions

- "What were the key business insights?"
- "Which columns had missing values?"
- "Show statistical findings."
- "What trends were detected?"

---

# State Management

Centralized workflow state management is implemented using LangGraph StateGraph.

### Managed Workflow States

- Workflow execution state
- Insight approval state
- Human feedback state
- Visualization state
- Report state
- Chat memory state

---

# Design Patterns Used

- Multi-Agent Architecture
- Service Layer Pattern
- Factory Pattern
- Repository Pattern
- Stateful Workflow Orchestration
- Human-in-the-Loop Workflow
- Retrieval-Augmented Generation (RAG)

---

# Tech Stack

## Backend

- Python 3.11
- LangGraph
- LangChain
- ChromaDB

## Frontend

- Streamlit
- Plotly

## AI / NLP

- Groq LLM
- HuggingFace Embeddings
- Retrieval-Augmented Generation (RAG)

## Data Processing

- Pandas
- NumPy
- Scikit-learn

## Visualization

- Plotly
- Matplotlib
- Seaborn

---

# Current Capabilities

- Autonomous analytics workflow execution
- Dynamic chart generation
- Statistical analysis automation
- Human-approved business insights
- AI-generated analytics reports
- Conversational analytics assistant
- RAG-powered analytics querying
- Persistent vector database memory

---

# Challenges Addressed

- LangGraph workflow recursion handling
- Human-in-the-loop orchestration
- Streamlit rerender/state persistence
- Dynamic visualization rendering
- Token optimization for LLM prompts
- Dependency compatibility handling
- Vector database integration

---

# Future Improvements

- Multi-dataset support
- Multi-user analytics sessions
- Authentication and role-based approvals
- SQL-based analytics querying
- Scheduled report generation
- Dashboard export features
- Cloud deployment
- Agent memory optimization
