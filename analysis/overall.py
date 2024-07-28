"""
Module: Overall Analysis

This module provides comprehensive analysis tools for startup investment data.

- Total investment calculations
- Monthly and yearly trend analysis
- Sector, city, and investor-based analysis
"""

import pandas as pd

from dataset import startup


class Overall:

    def __init__(self):
        self.startup = startup

    def total_invested_amount(self):
        """
        Calculate the total amount invested across all startups.

        Returns:
            float
        """
        return round(self.startup["amount"].sum())

    def max_amount_infused(self):
        """
        Determine the maximum amount invested in a single startup.
        """
        result = self.startup.groupby("name")["amount"].max()
        sorted_result = result.sort_values(ascending=False)
        return sorted_result.head(1).values[0]

    def avg_ticket_size(self):
        """
        Calculate the average investment amount per startup.
        """
        return self.startup.groupby("name")["amount"].sum().mean()

    def total_funded_startup(self):
        """
        Count the total number of unique startups that received funding.
        """
        return self.startup["name"].nunique()

    def total_funding_mom(self):
        """
        Analyze the total funding amount on a month-over-month basis.

        Returns:
            pandas.DataFrame
        """
        temp_df = startup.groupby(["year", "month"])["amount"].sum().reset_index()
        temp_df["MM-YYYY"] = (
            temp_df["month"].astype("str") + "-" + temp_df["year"].astype("str")
        )
        temp_df.rename(columns={"amount": "Total Funding (In Crore Rs.)"}, inplace=True)
        return temp_df

    def total_funded_startup_mom(self):
        """
        Analyze the number of funded startups on a month-over-month basis.

        Returns:
            pandas.DataFrame
        """
        temp_df = startup.groupby(["year", "month"])["amount"].count().reset_index()
        temp_df["MM-YYYY"] = (
            temp_df["month"].astype("str") + "-" + temp_df["year"].astype("str")
        )
        temp_df.rename(columns={"amount": "Total Funded Startups"}, inplace=True)
        return temp_df

    def most_funded_sector(self):
        """
        Identify the top 10 sectors with the highest total funding.

        Returns:
            pandas.DataFrame
        """
        temp_df = startup.groupby("vertical")["amount"].sum().reset_index()
        most_funded_sectors = (
            temp_df[temp_df["amount"] != 0.0]
            .sort_values(by="amount", ascending=False)
            .head(10)
        )
        most_funded_sectors["amount"] = round(most_funded_sectors["amount"], 2)
        return most_funded_sectors

    def most_funded_type(self):
        """
        Identify the top 10 startup types with the highest total funding.

        Returns:
            pandas.DataFrame
        """
        temp_df = startup.groupby("type")["amount"].sum().reset_index()
        return (
            temp_df[temp_df["amount"] != 0.0]
            .sort_values(by="amount", ascending=False)
            .head(10)
        )

    def most_funded_cities(self):
        """
        Identify the top 10 cities with the highest total funding.

        Returns:
            pandas.DataFrame
        """
        temp_df = startup.groupby("city")["amount"].sum().reset_index()
        most_funded_city = temp_df[temp_df["amount"] != 0]

        # Combine Bangalore and Bengaluru data
        bangalore_total = most_funded_city.loc[
            most_funded_city["city"].isin(["Bangalore", "Bengaluru"]), "amount"
        ].sum()
        most_funded_city = most_funded_city[most_funded_city["city"] != "Bengaluru"]
        most_funded_city.loc[most_funded_city["city"] == "Bangalore", "amount"] = (
            bangalore_total
        )

        most_funded_city = most_funded_city.sort_values(
            by="amount", ascending=False
        ).head(10)
        most_funded_city["amount"] = round(most_funded_city["amount"], 2)
        return most_funded_city

    def most_funded_startups_yoy(self):
        """
        Identify the most funded startup for each year.

        Returns:
            pandas.DataFrame
        """
        most_funded_startup_yoy = (
            startup.groupby(["year", "name"])["amount"]
            .sum()
            .sort_values(ascending=False)
            .reset_index()
            .drop_duplicates("year", keep="first")
            .sort_values(by="year")
        )
        most_funded_startup_yoy.rename(
            columns={
                "year": "Year",
                "name": "StartUp Name",
                "amount": "Amount (In Crore Rs)",
            },
            inplace=True,
        )
        return most_funded_startup_yoy

    def top_investors(self):
        """
        Identify the top 10 investors based on their total investment amounts.

        Returns:
            pandas.DataFrame
        """
        # Create separate rows for each investor
        investor_list = []
        for _, row in startup.iterrows():
            for investor in row["investors"].split(", "):
                investor_list.append({**row, "investors": investor})
        new_df = pd.DataFrame(investor_list)

        top_investors = new_df.groupby("investors")["amount"].sum().reset_index()

        # Combine SoftBank Group and Softbank data
        softbank_total = top_investors.loc[
            top_investors["investors"].isin(["SoftBank Group", "Softbank"]), "amount"
        ].sum()
        top_investors = top_investors[top_investors["investors"] != "Softbank"]
        top_investors.loc[top_investors["investors"] == "SoftBank Group", "amount"] = (
            softbank_total
        )

        return top_investors.sort_values(by="amount", ascending=False).head(10)

    def funding_amount_year_month(self):
        """
        Create a pivot table of funding amounts by year and month.
        """
        df_agg = startup.groupby(["year", "month"])["amount"].sum().reset_index()
        return df_agg.pivot(index="year", columns="month", values="amount")
