from tools.visualization_tools import (
    create_histogram,
    create_boxplot,
    create_correlation_heatmap,
    create_scatter_plot,
    create_line_chart,
    create_bar_chart
)

import plotly.express as px


def visualization_agent(state):

    try:

        print(
            "\n[Visualization Agent Started]"
        )

        df = state["dataframe"]

        eda_results = (

            state["eda_results"]

            .get(
                "structured_data",
                {}
            )
        )

        visualizations = []

        numerical_columns = (
            eda_results.get(
                "numerical_columns",
                []
            )
        )

        categorical_columns = (
            eda_results.get(
                "categorical_columns",
                []
            )
        )

        datetime_columns = (
            eda_results.get(
                "datetime_columns",
                []
            )
        )

        if len(numerical_columns) >= 2:

            correlation_df = (
                df[numerical_columns]
                .corr()
            )

            heatmap = px.imshow(

                correlation_df,

                text_auto=True,

                title="Correlation Heatmap"
            )

            visualizations.append(

                {
                    "title":
                    "Correlation Heatmap",

                    "figure":
                    heatmap
                }
            )


        for column in numerical_columns[:2]:

            histogram = px.histogram(

                df,

                x=column,

                title=f"Histogram - {column}"
            )

            visualizations.append(

                {
                    "title":
                    f"Histogram - {column}",

                    "figure":
                    histogram
                }
            )


        for column in numerical_columns[:2]:

            boxplot = px.box(

                df,

                y=column,

                title=f"Boxplot - {column}"
            )

            visualizations.append(

                {
                    "title":
                    f"Boxplot - {column}",

                    "figure":
                    boxplot
                }
            )

        if len(numerical_columns) >= 2:

            scatter = px.scatter(

                df,

                x=numerical_columns[0],

                y=numerical_columns[1],

                title="Scatter Plot"
            )

            visualizations.append(

                {
                    "title":
                    "Scatter Plot",

                    "figure":
                    scatter
                }
            )

        if (

            len(datetime_columns) > 0

            and

            len(numerical_columns) > 0

        ):

            line_chart = px.line(

                df,

                x=datetime_columns[0],

                y=numerical_columns[0],

                title="Trend Analysis"
            )

            visualizations.append(

                {
                    "title":
                    "Trend Analysis",

                    "figure":
                    line_chart
                }
            )


        for column in categorical_columns[:2]:

            if df[column].nunique() <= 10:

                value_counts_df = (

                    df[column]
                    .value_counts()
                    .reset_index()
                )

                value_counts_df.columns = [

                    column,

                    "count"
                ]

                bar_chart = px.bar(

                    value_counts_df,

                    x=column,

                    y="count",

                    title=f"Bar Chart - {column}"
                )

                visualizations.append(

                    {
                        "title":
                        f"Bar Chart - {column}",

                        "figure":
                        bar_chart
                    }
                )
        state["visualizations"] = (
            visualizations
        )

        state["current_agent"] = (
            "visualization_agent"
        )

        print(
            "\nVisualization Completed"
        )

        return state

    except Exception as e:

        print(
            "\nVisualization Error:",
            e
        )

        state["errors"].append(
            str(e)
        )

        return state