import os
import sys

sys.path.append(

    os.path.abspath(
        os.path.dirname(__file__)
    )
)

from graph.workflow import graph


# --------------------------------------------------
# Helper
# --------------------------------------------------

def print_section(title):

    print("\n" + "=" * 70)

    print(title)

    print("=" * 70)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    # --------------------------------------------------
    # Dataset Input
    # --------------------------------------------------

    file_path = input(
        "\nEnter dataset path: "
    )

    if not os.path.exists(file_path):

        print(
            "\n❌ File not found."
        )

        return

    # --------------------------------------------------
    # Initial State
    # --------------------------------------------------

    initial_state = {

        "file_path": file_path,

        "dataframe": None,

        "dataset_summary": {},

        "eda_results": {},

        "cleaning_results": {},

        "statistical_results": {},

        "visualizations": [],

        "insights": "",

        "final_report": "",

        "current_agent": "",

        "workflow_complete": False,

        "errors": []
    }

    # --------------------------------------------------
    # Workflow Start
    # --------------------------------------------------

    print_section(
        "🚀 Starting Autonomous Analytics Workflow"
    )

    try:

        # --------------------------------------------------
        # Execute Graph
        # --------------------------------------------------

        result = graph.invoke(

            initial_state,

            config={

                "recursion_limit": 50
            }
        )

    except Exception as e:

        print(
            f"\n❌ Workflow Failed:\n{e}"
        )

        return

    # --------------------------------------------------
    # Workflow Complete
    # --------------------------------------------------

    print_section(
        "🎉 Workflow Completed Successfully"
    )

    # --------------------------------------------------
    # Dataset Summary
    # --------------------------------------------------

    print_section(
        "📌 Dataset Summary"
    )

    for key, value in result[
        "dataset_summary"
    ].items():

        print(f"\n{key}:")

        print(value)

    # --------------------------------------------------
    # EDA Results
    # --------------------------------------------------

    print_section(
        "🧠 EDA Results"
    )

    for key, value in result[
        "eda_results"
    ].items():

        print(f"\n{key}:")

        print(value)

    # --------------------------------------------------
    # Cleaning Results
    # --------------------------------------------------

    print_section(
        "🧹 Data Cleaning Results"
    )

    for key, value in result[
        "cleaning_results"
    ].items():

        print(f"\n{key}:")

        print(value)

    # --------------------------------------------------
    # Statistical Results
    # --------------------------------------------------

    print_section(
        "📈 Statistical Analysis Results"
    )

    for key, value in result[
        "statistical_results"
    ].items():

        print(f"\n{key}:")

        print(value)

    # --------------------------------------------------
    # Visualizations
    # --------------------------------------------------

    print_section(
        "📊 Generated Visualizations"
    )

    if result["visualizations"]:

        for path in result[
            "visualizations"
        ]:

            print(path)

    else:

        print(
            "\nNo Visualizations Generated"
        )

    # --------------------------------------------------
    # Insights
    # --------------------------------------------------

    print_section(
        "💡 Business Insights"
    )

    print(
        result["insights"]
    )

    # --------------------------------------------------
    # Final Report
    # --------------------------------------------------

    print_section(
        "📄 Final Analytics Report"
    )

    print(
        result["final_report"]
    )

    # --------------------------------------------------
    # Workflow Status
    # --------------------------------------------------

    print_section(
        "⚙ Workflow Status"
    )

    print(

        f"\nLast Executed Agent: "

        f"{result['current_agent']}"
    )

    print(

        f"\nWorkflow Complete: "

        f"{result['workflow_complete']}"
    )

    # --------------------------------------------------
    # Errors
    # --------------------------------------------------

    print_section(
        "❌ Errors"
    )

    if result["errors"]:

        for error in result["errors"]:

            print(error)

    else:

        print(
            "\n✅ No Errors Found"
        )


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":

    main()