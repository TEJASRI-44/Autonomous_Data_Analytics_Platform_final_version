import plotly.express as px
import streamlit as st


def should_generate_visualization(
    user_query
):

    visualization_keywords = [

        "chart",
        "graph",
        "plot",
        "visualize",
        "visualization",
        "histogram",
        "bar",
        "line",
        "scatter",
        "trend",
        "distribution"
    ]

    query = user_query.lower()

    return any(

        keyword in query

        for keyword in visualization_keywords
    )


def generate_visualization(

    user_query,

    dataframe
):

    query = user_query.lower()

    numerical_columns = (

        dataframe
        .select_dtypes(
            include=["int64", "float64"]
        )
        .columns
        .tolist()
    )

    categorical_columns = (

        dataframe
        .select_dtypes(
            include=["object"]
        )
        .columns
        .tolist()
    )

    # =========================
    # HISTOGRAM
    # =========================

    if (

        "histogram" in query

        and

        numerical_columns
    ):

        column = numerical_columns[0]

        fig = px.histogram(

            dataframe,

            x=column,

            title=f"Histogram - {column}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =========================
    # BAR CHART
    # =========================

    elif (

        "bar" in query

        and

        categorical_columns
    ):

        column = categorical_columns[0]

        value_counts = (

            dataframe[column]
            .value_counts()
            .reset_index()
        )

        value_counts.columns = [
            column,
            "count"
        ]

        fig = px.bar(

            value_counts,

            x=column,

            y="count",

            title=f"Bar Chart - {column}"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # =========================
    # SCATTER PLOT
    # =========================

    elif len(numerical_columns) >= 2:

        fig = px.scatter(

            dataframe,

            x=numerical_columns[0],

            y=numerical_columns[1],

            title="Scatter Plot"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )