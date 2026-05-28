from tools.validation_tools import (
    validate_dataset,
    validate_dataframe_structure
)

from tools.data_ingestion_tools import (
    load_dataset
)

from tools.profiling_tools import (
    generate_dataset_summary
)


def data_ingestion_agent(state):

    try:

        print(
            "\n[Data Ingestion Agent Started]"
        )

        file_path = state["file_path"]



        validate_dataset(file_path)

        df = load_dataset(file_path)
        validate_dataframe_structure(df)


        summary = generate_dataset_summary(df)

        summary_report = f"""

### Dataset Successfully Loaded

- Total Rows: {summary.get("rows")}
- Total Columns: {summary.get("columns")}

### Available Columns

{', '.join(summary.get("columns_list", []))}

### Dataset Information

The dataset has been successfully validated
and loaded into the analytics workflow.

Initial profiling and dataset analysis
have been completed successfully.

The dataset contains both numerical
and categorical information suitable
for analytics and visualization workflows.
"""

        state["dataframe"] = df

        state["dataset_summary"] = {

            "structured_data":
            summary,

            "summary_report":
            summary_report
        }

        state["current_agent"] = (
            "data_ingestion_agent"
        )

        print(
            "\nDataset Loaded Successfully"
        )

        return state

    except Exception as e:

        print(
            "\nData Ingestion Error:",
            e
        )

        state["errors"].append(
            str(e)
        )

        state["workflow_complete"] = True

        return state