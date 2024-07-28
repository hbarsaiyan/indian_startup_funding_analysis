"""
Investor Analysis Component

This module provides interactive visualizations and insights about an investor's investments
"""

import streamlit as st
import plotly.express as px

from analysis import Investor as InvestorAnalysis


class Investor:
    def __init__(self):
        self.investor_analysis = InvestorAnalysis()

    def recent_five_investments(self, investor_name):
        """
        Display the five most recent investments of the investor.
        """
        st.subheader(
            "Most Recent Investments",
            help=f"{investor_name}'s five most recent investments.",
        )
        st.dataframe(self.investor_analysis.recent_five_investments(investor_name))

    def _plot_pie_chart(self, data, values, names, title, help_text):
        """
        Helper method to plot a pie chart.

        Args:
            data (pd.DataFrame): The data to plot.
            values (str): The column name for pie slice sizes.
            names (str): The column name for pie slice labels.
            title (str): The title of the chart.
            help_text (str): The help text for the chart.
        """
        st.subheader(title, help=help_text)
        fig = px.pie(data, values=values, names=names)
        st.plotly_chart(fig, use_container_width=True)

    def plot_biggest_investment(self, investor_name):
        """
        Plot a bar chart of the investor's biggest investments in terms of amount.

        Args:
            investor_name (str): The name of the investor.
        """
        st.subheader(
            "Biggest Investments",
            help=f"{investor_name}'s biggest investments in terms of amount.",
        )
        biggest_investment_df = self.investor_analysis.biggest_investment(investor_name)
        fig = px.bar(biggest_investment_df, x="name", y="amount")
        st.plotly_chart(fig, use_container_width=True)

    def plot_invested_sector(self, investor_name):
        """
        Pie chart of the investor's most invested sector.
        """
        sector_df = self.investor_analysis.invested_sector(investor_name)
        self._plot_pie_chart(
            sector_df,
            "amount",
            "vertical",
            "Sector Invested in",
            f"{investor_name}'s most invested sector.",
        )

    def plot_invested_subsector(self, investor_name):
        """
        Pie chart of the investor's most invested subsector.
        """
        subsector_df = self.investor_analysis.invested_subsector(investor_name)
        self._plot_pie_chart(
            subsector_df,
            "amount",
            "subvertical",
            "Subsector Invested in",
            f"{investor_name}'s most invested subsector.",
        )

    def plot_invested_city(self, investor_name):
        """
        Pie chart of the investor's most invested city.
        """
        city_df = self.investor_analysis.invested_city(investor_name)
        self._plot_pie_chart(
            city_df,
            "amount",
            "city",
            "City Invested in",
            f"{investor_name}'s most invested city.",
        )

    def plot_invested_type(self, investor_name):
        """
        Pie chart of the investor's investment types.
        """
        investment_type_df = self.investor_analysis.invested_type(investor_name)
        self._plot_pie_chart(
            investment_type_df,
            "amount",
            "type",
            "Investment Type",
            f"{investor_name}'s stage of investments.",
        )

    def plot_yoy_investment(self, investor_name):
        """
        Line chart of the investor's year-on-year investments.
        """
        st.subheader(
            "YOY investment", help=f"{investor_name}'s year-on-year investments."
        )
        yoy_investment_df = self.investor_analysis.yoy_investment(investor_name)
        fig = px.line(yoy_investment_df, x="year", y="amount")
        st.plotly_chart(fig, use_container_width=True)

    def similar_investors(self, investor_name):
        """
        Displays the name of four similar investors.
        """
        similar_investors = self.investor_analysis.get_similar_investors(investor_name)

        st.subheader(
            "Similar Investors",
            help=f"These investors have invested in the same sectors as {investor_name}.",
        )
        st.write("")

        cols = st.columns(4)
        for i, col in enumerate(cols):
            with col:
                try:
                    st.write(similar_investors[i])
                except IndexError:
                    st.write("")
