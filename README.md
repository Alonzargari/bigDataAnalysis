<h1>Readme</h1>
Job Listings Data Analysis
Introduction
In this project, we analyze a dataset of job descriptions, which provides a comprehensive collection of job postings. The analysis is conducted using SQL queries on the dataset, where each query returns a "small" dataset that provides insights into the job market based on the specific question asked.

For this project, we use Python along with DuckDB, where we create and manage tables for analysis.

Tables Created in DuckDB:
A table for the original dataset.
A table containing 500 sampled rows from the original dataset.
A table for each query result dataset, representing different insights into the job market.
After running the queries, we use Python to copy only the small datasets (points 2 & 3) into a standard SQLite database.

Finally, we use Streamlit to create an interactive dashboard, which serves as a user-friendly visual interface. The dashboard displays the queries, insights derived from them, and visualizations (graphs) illustrating the data. Additionally, the user can view the 500-sample dataset from the original job listings dataset.

Python Files
duckdb_sqlite.py:
Executes the first part of the project, running queries on the dataset, loading tables into DuckDB, and copying the small datasets into an SQLite file.

dashboard_plots.py:
Gathers all the plots and visualizations for the query results.

dashboard_jobs_data.py:
Manages the Streamlit dashboard, displaying query results and calling the appropriate visualizations from dashboard_plots.py.
