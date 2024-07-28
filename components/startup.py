"""
Startup Analysis Component

This module contains a Streamlit component for analyzing startups.
It provides functionality to display similar startups based on a given startup name.
"""

import streamlit as st
from analysis import Startup as StartupAnalysis


class Startup:
    """
    Class representing a startup component for analysis in a Streamlit application.
    """

    def __init__(self):
        """
        Initializes a Startup object and its associated analysis.
        """
        self.startup_analysis = StartupAnalysis()

    def similar_startups(self, startup_name: str):
        """
        Displays similar startups in the Streamlit application for a given startup name.
        """
        similar_startups = self.startup_analysis.similar_startups(startup_name)

        self._display_similar_startups_header(startup_name)
        self._display_similar_startups_list(similar_startups)

    def _display_similar_startups_header(self, startup_name: str):
        """
        Displays the header for the similar startups section.
        """
        st.subheader(
            "Similar Startups",
            help=f"These startups belong to the same sector as {startup_name}.",
        )
        st.write("")

    def _display_similar_startups_list(self, similar_startups: list):
        """
        Displays the list of similar startups in a 4-column layout.
        """
        cols = st.columns(4)
        for i, col in enumerate(cols):
            with col:
                try:
                    st.write(similar_startups[i])
                except IndexError:
                    st.write("")


if __name__ == "__main__":
    startup = Startup()
    startup.similar_startups("Example Startup")
