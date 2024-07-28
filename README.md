# Indian Startup Investment Analysis

This project aims to provide comprehensive visualizations and analysis of the Indian startup funding dataset using Pandas, Plotly, and Streamlit. It offers interactive plots and informative tooltips to explore various aspects of startup investments and investors.

## Project Overview

This project aims to analyze and visualize the Indian startup funding dataset. It provides a web-based interface built with Streamlit, allowing users to explore the dataset and gain insights through interactive plots and metrics. The project utilizes Pandas and Plotly libraries for data manipulation and visualization, respectively.

The main objectives of this project are:

1. Perform an overall analysis of the startup funding ecosystem in India.
2. Enable analysis of individual startups based on user selection.
3. Provide insights into individual investors based on user selection.

## Dataset

The dataset used in this project is sourced from Kaggle and is provided by Sudalai Rajkumar.

Link: [Indian Startup Funding Dataset](https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding)

## Data Cleaning

The dataset has been cleaned using the code in `dataset_cleaning` Jupyter notebook.

# Data Analysis

We then analyze the dataset using the Plotly and WordCloud in `eda` Jupyter notebook.

## Structure

The website consists of three main sections: Overall Analysis, Startup Analysis, and Investor Analysis. Each section offers different visualizations and insights based on the selected data.

### 1. Overall Analysis

- Month-by-month metrics (total investments, maximum investment, average investment, total funded startups)
- Line graphs for monthly funding trends
- Top 10 visualizations (funded sectors, investors, startups, cities, round types)
- 3D bar graph for top funded startups year-on-year

### 2. Startup Analysis

- Detailed information on user-selected startup
- Metrics: total investments, sector, subsector, funding stage, investors
- List of similar startups in the same sector

### 3. Investor Analysis

- Detailed information on user-selected investor
- Recent investments data
- Visualizations:
  - Biggest investments (bar chart)
  - Most invested city, sector, subsector, investment type (pie charts)
  - Year-on-year investment trend (line graph)
- List of investors in similar sectors
