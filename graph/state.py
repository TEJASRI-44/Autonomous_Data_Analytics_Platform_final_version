from typing import TypedDict
import pandas as pd


class AnalyticsState(TypedDict):

    file_path: str
    dataframe: pd.DataFrame
    dataset_summary: dict
    eda_results: dict
    cleaning_results: dict
    statistical_results: dict
    visualizations: list
    insights: str
    final_report: str
    current_agent: str
    workflow_complete: bool
    errors: list 
    report_path:str
    approval_status: str
    human_feedback: str