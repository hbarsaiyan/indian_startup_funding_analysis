"""
Classes:
- PlotChart: Base class for plotting charts.
- PlotHorizontalBarChart: Class for plotting a horizontal bar chart (inherits from PlotChart).
- PlotLineChart: Class for plotting a line chart (inherits from PlotChart).
- SubHeader: Class for displaying a subheader with a tooltip.
- Overall: Class for handling overall analysis and plotting of startup data.
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from analysis import Overall as OverallAnalysis


class PlotChart:
    """Base class for plotting charts."""

    def __init__(self, title: str):
        """
        Initialize the PlotChart class.

        Args:
            title (str): The title of the chart.
        """
        self.title = title

    def plot(self, fig):
        """
        Plot the chart using Streamlit.

        Args:
            fig: The plotly figure object to be plotted.
        """
        st.plotly_chart(fig, use_container_width=True)


class PlotHorizontalBarChart(PlotChart):
    """Class to plot a horizontal bar chart."""

    def __init__(
        self,
        x_axis: pd.Series,
        y_axis: pd.Series,
        title: str,
        x_label: str,
        y_label: str,
    ):
        """
        Initialize the PlotHorizontalBarChart class.

        Args:
            x_axis (pd.Series): The x-axis data.
            y_axis (pd.Series): The y-axis data.
            title (str): The title of the chart.
            x_label (str): The label for the x-axis.
            y_label (str): The label for the y-axis.
        """
        super().__init__(title)
        fig = go.Figure(data=go.Bar(x=x_axis, y=y_axis, orientation="h"))
        fig.update_layout(
            title=title, xaxis=dict(title=x_label), yaxis=dict(title=y_label)
        )
        self.plot(fig)


class PlotLineChart(PlotChart):
    """Class to plot a line chart."""

    def __init__(self, df: pd.DataFrame, x_axis: str, y_axis: str, title: str):
        """
        Initialize the PlotLineChart class.

        Args:
            df (pd.DataFrame): The dataframe containing the chart data.
            x_axis (str): The column name for the x-axis.
            y_axis (str): The column name for the y-axis.
            title (str): The title of the chart.
        """
        super().__init__(title)
        fig = px.line(df, x=x_axis, y=y_axis, title=title)
        self.plot(fig)


class SubHeader:
    """Class to display a subheader with a tooltip."""

    def __init__(self, title: str, tooltip: str):
        """
        Args:
            title (str): The title of the subheader.
            tooltip (str): The tooltip text.
        """
        st.subheader(title, help=tooltip)


class Overall:
    def __init__(self):
        self.overall_analysis = OverallAnalysis()

    def plot_total_funding_mom(self):
        """Plot the total amount of funding in Indian startups month over month."""
        temp_df = self.overall_analysis.total_funding_mom()
        SubHeader(
            "Total Amount of Funding in Indian Startups MoM",
            "Total Amount of Funding in Indian Startups on the basis of month and year",
        )
        PlotLineChart(
            temp_df,
            "MM-YYYY",
            "Total Funding (In Crore Rs.)",
            "Total funding in Startups in MM-YYYY",
        )

    def plot_total_funded_startup_mom(self):
        """Plot the total number of funded Indian startups MoM."""
        temp_df = self.overall_analysis.total_funded_startup_mom()
        SubHeader(
            "Total Funded Indian Startups MoM",
            "Total Funded Indian Startups on the basis of month and year",
        )
        PlotLineChart(
            temp_df,
            "MM-YYYY",
            "Total Funded Startups",
            "Total Funded Startups in MM-YYYY",
        )

    def plot_most_funded_sector(self):
        """Plot the top 10 most funded sectors between 2015 to 2020."""
        most_funded_sectors = self.overall_analysis.most_funded_sector()
        SubHeader(
            "Most Funded Sectors", "Top 10 Most Funded Sectors between 2015 to 2020"
        )
        PlotHorizontalBarChart(
            most_funded_sectors["amount"],
            most_funded_sectors["vertical"],
            "Top 10 Most Funded Sectors",
            "Funding Amount (In Crore Rs)",
            "Sector",
        )

    def plot_most_funded_type(self):
        """Plot the top 10 most funded types of rounds in startup funding."""
        most_funded_type = self.overall_analysis.most_funded_type()
        SubHeader(
            "Most Funded Type", "Top 10 most funded type of round in startup funding"
        )
        PlotHorizontalBarChart(
            most_funded_type["amount"],
            most_funded_type["type"],
            "Top 10 Most Funded Types of Rounds",
            "Funding Amount (In Crore Rs)",
            "Type of Investment",
        )

    def plot_most_funded_cities(self):
        """Plot the top 10 most funded cities in startup funding."""
        most_funded_city = self.overall_analysis.most_funded_cities()
        SubHeader("Most Funded Cities", "Top 10 most funded cities in startup funding")
        PlotHorizontalBarChart(
            most_funded_city["amount"],
            most_funded_city["city"],
            "Most Funded Cities",
            "Funding Amount (In Crore Rs)",
            "City",
        )

    def plot_most_funded_startups_yoy(self):
        """Plot the top 10 most funded startups year over year."""
        most_funded_startup_yoy = self.overall_analysis.most_funded_startups_yoy()
        SubHeader(
            "Most Funded Startups YoY",
            "Top 10 most funded startups in startup funding YoY",
        )
        fig = px.bar(
            most_funded_startup_yoy,
            x="StartUp Name",
            y="Amount (In Crore Rs)",
            color="Year",
        )
        st.plotly_chart(fig, use_container_width=True)

    def plot_top_investors(self):
        """Plot the top investors based on their investment values."""
        top_investors = self.overall_analysis.top_investors()
        SubHeader(
            "Top Investors",
            "Top most investors on the basis of their investment values.",
        )
        PlotHorizontalBarChart(
            top_investors["amount"],
            top_investors["investors"],
            "Top Most Investors",
            "Funding Amount (In Crore Rs)",
            "Investor",
        )

    def plot_funding_amount_year_month(self):
        """Plot the funding amount by year and month."""
        pivot_table = self.overall_analysis.funding_amount_year_month()
        SubHeader(
            "Year and Month Funding",
            "Heatmap to show the funding amount by year and month.",
        )
        heatmap = go.Heatmap(
            x=pivot_table.columns,
            y=pivot_table.index,
            z=pivot_table.values,
            colorscale="Viridis",
        )
        layout = go.Layout(
            title="Funding Amount by Year and Month",
            xaxis={"title": "Month"},
            yaxis={"title": "Year"},
        )
        fig = go.Figure(data=[heatmap], layout=layout)
        st.plotly_chart(fig, use_container_width=True)
