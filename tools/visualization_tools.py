import os

import matplotlib.pyplot as plt
import seaborn as sns

from services.visualization_service import (
    VisualizationService
)


os.makedirs(
    "visualizations",
    exist_ok=True
)

plt.ioff()

sns.set_style("whitegrid")


# --------------------------------------------------
# Common Save Utility
# --------------------------------------------------

def save_and_close_plot(output_path):

    plt.tight_layout()

    plt.savefig(

        output_path,

        dpi=80,

        bbox_inches="tight"
    )

    plt.close()


# --------------------------------------------------
# Histogram
# --------------------------------------------------

def create_histogram(df, column):

    plt.figure(figsize=(4, 3))

    sns.histplot(

        data=df,

        x=column,

        kde=True,

        bins=20

    )

    plt.title(
        f"{column} Distribution"
    )

    output_path = (

    VisualizationService
        .get_visualization_path(

            f"{column}_histogram.png"
        )
    )
    save_and_close_plot(
        output_path
    )

    return output_path


# --------------------------------------------------
# Boxplot
# --------------------------------------------------

def create_boxplot(df, column):

    plt.figure(figsize=(4, 3))

    sns.boxplot(
        y=df[column]
    )

    plt.title(
        f"{column} Outliers"
    )
    output_path=(VisualizationService
    .get_visualization_path(

        f"{column}_boxplot.png"
    )
    )

    save_and_close_plot(
        output_path
    )

    return output_path


# --------------------------------------------------
# Correlation Heatmap
# --------------------------------------------------

def create_correlation_heatmap(df):

    numerical_df = (

        df.select_dtypes(
            include=["int64", "float64"]
        )

    )

    # Skip if insufficient numerical columns

    if numerical_df.shape[1] < 2:

        return None

    correlation = (
        numerical_df.corr()
    )

    plt.figure(figsize=(5, 4))

    sns.heatmap(

        correlation,

        annot=True,

        fmt=".2f",

        cmap="coolwarm",

        cbar=False
    )

    plt.title(
        "Correlation Heatmap"
    )

    output_path = (
        "visualizations/correlation_heatmap.png"
    )
    
    save_and_close_plot(
        output_path
    )

    return output_path


# --------------------------------------------------
# Scatter Plot
# --------------------------------------------------

def create_scatter_plot(df, x_column, y_column):

    plt.figure(figsize=(4, 3))

    sns.scatterplot(

        data=df,

        x=x_column,

        y=y_column
    )

    plt.title(
        f"{x_column} vs {y_column}"
    )

    output_path=(VisualizationService
    .get_visualization_path(

        f"scatter.png"
    )
    )
    save_and_close_plot(
        output_path
    )

    return output_path


# --------------------------------------------------
# Line Chart
# --------------------------------------------------

def create_line_chart(df, x_column, y_column):

    plt.figure(figsize=(5, 3))

    sns.lineplot(

        data=df,

        x=x_column,

        y=y_column
    )

    plt.xticks(rotation=45)

    plt.title(
        f"{y_column} Trend"
    )

    output_path=(VisualizationService
    .get_visualization_path(

        f"trend.png"
    )
    )
    save_and_close_plot(
        output_path
    )

    return output_path


# --------------------------------------------------
# Bar Chart
# --------------------------------------------------

def create_bar_chart(df, column):

    plt.figure(figsize=(5, 3))

    (

        df[column]

        .value_counts()

        .head(8)

        .plot(
            kind="bar"
        )
    )

    plt.title(
        f"{column} Distribution"
    )

    output_path=(VisualizationService
    .get_visualization_path(

        f"{column}_barchart.png"
    )
    )

    save_and_close_plot(
        output_path
    )

    return output_path