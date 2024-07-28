"""
Key features:
- Retrieval of specific startup information (sector, funding, investors, etc.)
- Identification of similar startups based on sector

Note: Existence of a 'startup_cleaned.csv' file in the 'dataset' directory is necessary.
"""

import pandas as pd

# Load and preprocess the startup data
startup = pd.read_csv("dataset/startup_cleaned.csv")
startup["date"] = pd.to_datetime(startup["date"])
startup["year"] = startup["date"].dt.year
startup["month"] = startup["date"].dt.month


class Startup:
    """
    Attributes:
        startup (pandas.DataFrame): The preprocessed startup dataset.

    Methods:
        list_of_startups: Retrieve a sorted list of all startup names.
        sector: Get the sector of a specific startup.
        subsector: Get the subsector of a specific startup.
        location: Get the city location of a specific startup.
        stage: Get the funding stage of a specific startup.
        investors: Get the investors of a specific startup.
        investment_date: Get the investment date for a specific startup.
        funding: Calculate the total funding amount for a specific startup.
        similar_startups: Find startups in the same sector as a given startup.
    """

    def __init__(self):
        self.startup = startup

    def list_of_startups(self):
        """
        Retrieve a sorted list of all unique startup names in the dataset.
        """
        return sorted(startup["name"].unique())[1:]

    def sector(self, startup_name):
        """
        Get the main sector (vertical) of a specific startup.
        """
        return self.startup[self.startup["name"] == startup_name]["vertical"].values[0]

    def subsector(self, startup_name):
        """
        Get the subsector (subvertical) of a specific startup.

        Args:
            startup_name (str): The name of the startup.

        Returns:
            str: The subsector of the startup.
        """
        return self.startup[self.startup["name"] == startup_name]["subvertical"].values[
            0
        ]

    def location(self, startup_name):
        """
        Get the city location of a specific startup.
        """
        return self.startup[self.startup["name"] == startup_name]["city"].values[0]

    def stage(self, startup_name):
        """
        Get the funding stage or type of a specific startup.
        """
        return self.startup[self.startup["name"] == startup_name]["type"].values[0]

    def investors(self, startup_name):
        """
        Get the list of investors for a specific startup.
        """
        return self.startup[self.startup["name"] == startup_name]["investors"].values[0]

    def investment_date(self, startup_name):
        """
        Get the investment date for a specific startup.
        """
        return self.startup[self.startup["name"] == startup_name]["date"].values[0]

    def funding(self, startup_name):
        """
        Calculate the total funding amount for a specific startup.
        """
        return self.startup[self.startup["name"] == startup_name]["amount"].sum()

    def similar_startups(self, startup_name):
        """
        Find startups operating in the same sector as the given startup.

        This method identifies other startups that share the same vertical (main sector)
        as the specified startup, excluding the startup itself from the results.
        """
        vertical = self.startup.loc[
            self.startup["name"] == startup_name, "vertical"
        ].values[0]
        return [
            name
            for name in self.startup[self.startup["vertical"] == vertical][
                "name"
            ].unique()
            if name != startup_name
        ]
