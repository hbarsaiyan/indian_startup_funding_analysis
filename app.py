"""
Streamlit Web Application

"""

import streamlit as st

from analysis import (
    Investor as InvestorAnalysis,
    Overall as OverallAnalysis,
    Startup as StartupAnalysis,
)

from components import (
    Investor as InvestorComponent,
    Overall as OverallComponent,
    Startup as StartupComponent,
)

from components import PADDING_TOP


class Main:
    """
    Main class

    This class handles the main UI logic.
    """

    def __init__(self):
        """
        Initialize the Main class.

        This method sets up all necessary analysis and component instances.
        """
        self.investor_analysis = InvestorAnalysis()
        self.investor_component = InvestorComponent()
        self.overall_analysis = OverallAnalysis()
        self.overall_component = OverallComponent()
        self.startup_analysis = StartupAnalysis()
        self.startup_component = StartupComponent()
        self.setup_page()
        self.render_sidebar()
        self.route_to_component()

    def setup_page(self):
        """
        Set up the main page configuration.

        This method configures the page layout, title, and icon.
        """
        st.set_page_config(
            layout="wide",
            page_title="Indian Startup Investment Analysis",
            page_icon="📊",
        )

    def render_sidebar(self):
        """
        Render the sidebar with navigation options.

        This method creates the sidebar title and the selection box for different analysis options.
        """
        st.sidebar.title(
            "Indian Startup Investment Analysis",
            help="Note: Data for Indian Startups (2015-2020)",
        )
        self.selected_option = st.sidebar.selectbox(
            "Select One", ["Overall Analysis", "Startup", "Investor"]
        )

    def route_to_component(self):
        """
        Route to the appropriate component based on user selection.
        """
        if self.selected_option == "Overall Analysis":
            self.render_overall_analysis()
        elif self.selected_option == "Startup":
            self.render_startup_analysis()
        elif self.selected_option == "Investor":
            self.render_investor_analysis()

    def render_overall_analysis(self):
        """
        This method handles the UI and logic
        """
        self.render_header("Overall Analysis")
        self.render_mom_analysis()
        self.render_mom_graph()
        self.overall_component.plot_most_funded_sector()
        self.overall_component.plot_top_investors()
        self.overall_component.plot_most_funded_startups_yoy()
        self.overall_component.plot_most_funded_cities()
        self.overall_component.plot_most_funded_type()
        self.overall_component.plot_funding_amount_year_month()

    def render_mom_analysis(self):
        """
        Render the Month-over-Month (MoM) analysis section.
        """
        st.header("MoM Analysis", help="Month-over-Month (MoM) Analysis.")
        st.divider()
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total",
                f"{self.overall_analysis.total_invested_amount()} Cr",
                delta="50 Cr",
            )
        with col2:
            st.metric("Maximum", f"{self.overall_analysis.max_amount_infused()} Cr")
        with col3:
            st.metric(
                "Average",
                f"{round(self.overall_analysis.avg_ticket_size())} Cr",
                delta="20 Cr",
            )
        with col4:
            st.metric(
                "Total Funded Startups",
                self.overall_analysis.total_funded_startup(),
                delta="10",
            )

    def render_mom_graph(self):
        """
        Render the Month-over-Month (MoM) graph section.
        """
        st.divider()
        st.header("MoM Graph", help="Month-over-Month (MoM) graph analysis")
        st.divider()

        selected_option = st.selectbox(
            "Select Type of MoM chart",
            ["Total Amount of Funding MoM", "Total Funded Indian Startups MoM"],
        )

        st.divider()
        if selected_option == "Total Amount of Funding MoM":
            self.overall_component.plot_total_funding_mom()
        else:
            self.overall_component.plot_total_funded_startup_mom()

    def render_startup_analysis(self):
        """
        Render the individual startup analysis component.
        """
        self.render_header("Startup Analysis")
        startup_name = st.sidebar.selectbox(
            "Select Startup", self.startup_analysis.list_of_startups()
        )
        btn = st.sidebar.button("Find Startup details")

        if btn:
            self.render_startup_details(startup_name)

    def render_startup_details(self, startup_name):
        st.subheader(
            f"{startup_name} Analysis", help=f"Overall Analysis of {startup_name}"
        )
        st.metric(
            "Investments (In Crore Rs)",
            self.startup_analysis.funding(startup_name),
            delta="+10",
        )
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Sector", self.startup_analysis.sector(startup_name))
            st.metric("Stage", self.startup_analysis.stage(startup_name))
        with col2:
            st.metric("Subsector", self.startup_analysis.subsector(startup_name))
            st.metric("Investors", self.startup_analysis.investors(startup_name))

        st.divider()
        self.startup_component.similar_startups(startup_name)

    def render_investor_analysis(self):
        """
        Render the investor analysis component.

        This method handles the UI and logic for analyzing individual investors,
        including selection, investments, and similar investors.
        """
        self.render_header("Investor Detail")
        investor_name = st.sidebar.selectbox(
            "Select Investor", self.investor_analysis.investor_list()
        )
        btn = st.sidebar.button("Find Investor details")

        st.title(investor_name)
        st.divider()

        if btn:
            self.render_investor_details(investor_name)

    def render_investor_details(self, investor_name):
        """
        Render the details for a specific investor.
        """
        self.investor_component.recent_five_investments(investor_name)
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            self.investor_component.plot_biggest_investment(investor_name)
            self.investor_component.plot_invested_sector(investor_name)
            self.investor_component.plot_invested_type(investor_name)
        with col2:
            self.investor_component.plot_invested_city(investor_name)
            self.investor_component.plot_invested_subsector(investor_name)
            self.investor_component.plot_yoy_investment(investor_name)

        st.divider()
        self.investor_component.similar_investors(investor_name)

    def render_header(self, title):
        """
        Adds custom padding at the top and centers the header title.
        """
        st.markdown(PADDING_TOP, unsafe_allow_html=True)
        _, col, _ = st.columns(3)
        with col:
            st.header(title)
        st.divider()


if __name__ == "__main__":
    Main()
