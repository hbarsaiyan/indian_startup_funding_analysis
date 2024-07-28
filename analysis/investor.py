"""

This module provides functionality for analyzing investor data in the startup dataset.

It offers various methods to extract and analyze
investor-related information from the startup data.
"""

import itertools
import random
import pandas as pd

from dataset import startup


class Investor:
    """
    Attributes:
        startup (pandas.DataFrame): The startup dataset.

    Methods:
        investor_list: Retrieve a sorted list of all investors.
        recent_five_investments: Get the five most recent investments for a given investor.
        biggest_investment: Find the largest investments made by an investor.
        invested_sector: Analyze the sectors an investor has invested in.
        invested_subsector: Examine the sub-sectors an investor has invested in.
        invested_city: Identify the cities where an investor has made investments.
        invested_type: Categorize the types of investments made by an investor.
        yoy_investment: Calculate the year-over-year investment trends for an investor.
        get_similar_investors: Identify investors with similar investment patterns.
    """

    def __init__(self):
        self.startup = startup

    def investor_list(self):
        """
        Generate a sorted list of all unique investors in the dataset.
        """
        return sorted(set(self.startup["investors"].str.split(",").sum()))[2:]

    def recent_five_investments(self, investor_name):
        """
        Retrieve details of the five most recent investments made by a specific investor.
        """
        recent_investment = (
            self.startup[self.startup["investors"].str.contains(investor_name)]
            .head()[["date", "name", "vertical", "city", "investors", "type", "amount"]]
            .rename(
                columns={
                    "date": "Date of Investment",
                    "name": "Startup Name",
                    "vertical": "Vertical",
                    "city": "City",
                    "investors": "Investors",
                    "type": "Type",
                    "amount": "Amount (In crore ₹)",
                }
            )
        )

        return recent_investment

    def biggest_investment(self, investor_name):
        """
        Identify the largest investments made by a specific investor.
        """
        investments = self.startup[
            self.startup["investors"].str.contains(investor_name)
        ]
        investments_grouped = investments.groupby("name")["amount"].sum()
        sorted_investments = investments_grouped.sort_values(ascending=False)
        top_investments = sorted_investments.head().reset_index()

        return top_investments

    def invested_sector(self, investor_name):
        """
        Analyze the sectors in which a specific investor has made investments.
        """
        investments = startup[startup["investors"].str.contains(investor_name)]
        investments_grouped = investments.groupby("vertical")["amount"].sum()
        investments_sum_by_vertical = investments_grouped.reset_index()

        return investments_sum_by_vertical

    def invested_subsector(self, investor_name):
        """
        Examine the sub-sectors in which a specific investor has made investments.
        """
        investments = startup[startup["investors"].str.contains(investor_name)]
        investments_grouped = investments.groupby("subvertical")["amount"].sum()
        investments_sum_by_subvertical = investments_grouped.reset_index()

        return investments_sum_by_subvertical

    def invested_city(self, investor_name):
        """
        Identify the cities where a specific investor has made investments.
        """
        investments = startup[startup["investors"].str.contains(investor_name)]
        investments_grouped = investments.groupby("city")["amount"].sum()
        investments_sum_by_city = investments_grouped.reset_index()

        return investments_sum_by_city

    def invested_type(self, investor_name):
        """
        Categorize the types of investments made by a specific investor.
        """
        investments = startup[startup["investors"].str.contains(investor_name)]
        investments_grouped = investments.groupby("type")["amount"].sum()
        investments_sum_by_type = investments_grouped.reset_index()

        return investments_sum_by_type

    def yoy_investment(self, investor_name):
        """
        Calculate the YoY investment trends for a specific investor.
        """
        investments = startup[startup["investors"].str.contains(investor_name)]
        investments_grouped = investments.groupby("year")["amount"].sum()
        investments_sum_by_year = investments_grouped.reset_index()

        return investments_sum_by_year

    def get_similar_investors(self, investor_name):
        """
        Identify investors with similar investment patterns based on sector.
        """
        investor_df = startup[startup["investors"].str.contains(investor_name)]

        if investor_df.empty:
            return pd.Series()

        investor_vertical = investor_df["vertical"].iloc[0]

        vertical_df = self.startup[
            (self.startup["vertical"] == investor_vertical)
            & (
                ~self.startup["investors"].str.contains(
                    "Undisclosed Investors", case=False
                )
            )
        ]

        vertical_df = vertical_df[vertical_df["investors"] != investor_name]

        nested_list = sorted(vertical_df["investors"].str.split(","))
        flattened_list = list(itertools.chain.from_iterable(nested_list))
        try:
            return random.sample(flattened_list, 4)
        except ValueError:
            return flattened_list
