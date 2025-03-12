# ---------------- Big Data: Last Exercise-----------------------
# Submitting:
# Re'em Hoisman - 211694146
# Alon Zargari - 208626515

"""
This file is an interactive Streamlit dashboard designed for visual analysis
of the job market data. It loads data from an SQLite database and presents
insights on job postings
"""

import sqlite3
import pandas as pd
import dashboard_plots as dp
import streamlit as st


def configure_page():

    """Sets up the Streamlit page layout and applies custom styling."""

    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
    .big-font {
        font-size:20px;
    }
    </style>
    """, unsafe_allow_html=True)


def load_data():

    """Loads job market data from an SQLite database into Pandas dataframes."""

    conn = sqlite3.connect('db_file.sqlite')
    sample_jobs_data = pd.read_sql("SELECT * FROM SampleJobsData", conn)
    top_countries_job_posts = pd.read_sql("SELECT * FROM TopCountriesJobPosts", conn)
    min_exp = pd.read_sql("SELECT * FROM MinimumExperience", conn)
    discrimination = pd.read_sql("SELECT * FROM Discrimination", conn)
    job_market_ratings = pd.read_sql("SELECT * FROM JobMarketRatings", conn)
    under_minimum = pd.read_sql("SELECT * FROM UnderMinimum", conn)
    conn.close()
    return sample_jobs_data, top_countries_job_posts, min_exp, discrimination, job_market_ratings, under_minimum


def display_page_layout(title, question, content_text, plot_func, df):

    """Creates a structured page layout with a title, insights, table, and visualization."""

    st.title(title)
    st.divider()
    st.subheader(question)
    col1, _, col2 = st.columns([1.5, 0.2, 1])
    with col1:
        st.markdown(f"<div class='big-font'><u>Insights: </u>{content_text}</div>", unsafe_allow_html=True)
    with col2:
        st.dataframe(df)
    st.divider()
    st.subheader("Visualization")
    plot_func(df)


def story_page():

    """Displays an introduction explaining how data analysis can help job seekers."""

    story = """
        In today's world, finding a job is not just about sending out resumes – it's a complex process influenced by many factors:<br>
        supply and demand in the market, experience requirements, salary, location, and gender preferences. All these factors can affect the chances of finding the right job at the right time.<br><br>
        Job seekers are often interested in labor market research and may have many questions:<br>
        * How many job openings are posted in the leading economies of the world? Where does Israel stand in comparison, and which companies are the leaders in these countries?<br>
        * Does experience really matter? Candidates starting out might find that most jobs require experience, but are there industries willing to train new employees?<br>
        * What about salary? No one wants to work for a low salary, but is there really a difference between companies? Do big companies pay more than small ones?<br>
        * Gender discrimination – myth or reality? Are there jobs aimed at a specific gender? Are certain industries more open to women or men?<br>
        * Where is it most worthwhile to search? There are many job search platforms, but which ones actually post the most job openings?<br><br>
        To answer these questions, we did a big data analysis that can give us a clear picture of work market. 
    """
    st.title("Story")
    st.divider()
    st.subheader("How Can Data Help Us Find a Job?")
    st.markdown(f"<div class='big-font'>{story}</div>", unsafe_allow_html=True)


def under_min_salary_page(df):

    """Analyzes and visualizes job postings that offer below-average salaries."""

    title = "Under minimum salary posts per company"
    question = "How many job postings does each company have (if any) where the offered minimum wage is below the average minimum wage in the market?"
    into_text = """
                The table, graph, and word cloud provided below display the companies that offer salaries below the average.
                This information is important because it helps us identify where pay gaps exist, which can affect how happy and committed employees are.
                The size of each word could depends the amount of jobs that its posts with under minimum salary offer 
                """
    display_page_layout(title, question, into_text, dp.under_min_salary_plot, df)


def Recruiters_portals_page(df):

    """Displays the top job posting websites and their most active recruiters."""

    title = "Top rated portals and recruiters"
    question = "What are the top five job sites by number of postings, and who are the top three recruiters on each site with their job counts??"
    into_text = """
                The table gives a clear view of the top five job posting websites, showing which ones are most popular and work best for finding jobs.
                It also lists the top three recruiters for each website, pointing out the key people in the job market. This information is important
                for job seekers and employers because it helps them focus on the websites and people that can best help them reach their work goals.
                """
    display_page_layout(title, question, into_text, dp.recruiters_portal_ranking_plots, df)


def discrimination_posts_page(df):

    """Examines gender-based job posting preferences across different countries."""

    title = "Discrimination posts"
    question = "For each level of qualification, how many jobs are there for male, female, or both in each country?"
    into_text = """
            Our dataset contains a column with the name: "preferences" which means - 
            the work place (company) prefer hiring a women/men/both.
            If we look at the bigger picture, without focusing on specific companies, we can see the number of job posts in each country with certain preferences. 
            This information can reveal a lot about how each country discriminates against specific genders, or not.
            in this table we shows you the a amount of jobs that publish for each "preference"
            """
    display_page_layout(title, question, into_text, dp.discrimination_posts_plot, df)


def min_experience_page(df):

    """Shows job availability over the years for candidates with minimal experience."""

    title = "Minimum experience"
    question = "How many job posts were available each year for individuals with 0 to 2 years of experience?"
    into_text = """
         Advancements in technology, wars, and company budgets are just a few of the many factors that cause
         changes in job market requirements. New graduates often find it challenging to secure employment. 
         The following table displays the number of job openings available each year for individuals with 
         0 to 2 years of experience and any qualification.
        """

    display_page_layout(title, question, into_text, dp.min_experience_plot, df)


def top_country_jobs_page(df):

    """Compares job postings across the world's leading economies and Israel."""

    title = "Top Companies in Leading Countries"
    question = "How many job openings are posted in the world’s leading economies, where does Israel stand in comparison to them, and who are their top five leading companies?"
    into_text = """
         The question helps us understand the global job market and compare leading economic countries with Israel.
         The number of job openings in each country shows the economic growth and the demand for workers in different areas.
         The leading companies highlight trends in various industries.
        """

    display_page_layout(title, question, into_text, dp.leading_countries_job_posts, df)


def home_page(df):

    """Provides an overview of the dataset and displays sample job data."""

    text = """
        This dataset includes a collection of simulated job advertisements created for research purposes.
        The goal is to assist researchers and academics in analyzing job market trends.
        It contains a variety of job postings in different industries and for various types of positions.
    """
    st.title("📊 Jobs Data Dashboard")
    st.divider()
    st.markdown("## Overview 📑")
    st.markdown(f"<div class='big-font'>{text}</div>", unsafe_allow_html=True)
    st.caption(
        "the dataset is `job_descriptions.csv`. link to the website [Job Dataset](https://www.kaggle.com/datasets/ravindrasinghrana/job-description-dataset)")
    st.dataframe(df)
    st.caption("submitting: Re'em Hoisman- 211694146 and Alon Zargari - 208626515")


def main():
    """Initializes the dashboard, loads data, and manages page navigation."""

    configure_page()
    sample_jobs_data, top_country_jobs, min_exp, discrimination, job_market_ratings, under_minimum = load_data()
    st.sidebar.title("Pages Menu")

    page_functions = {
        "Home": (home_page, sample_jobs_data),
        "Top Companies in Leading Countries": (top_country_jobs_page, top_country_jobs),
        "Minimum experience distribution": (min_experience_page, min_exp),
        "Discrimination posts": (discrimination_posts_page, discrimination),
        "Recruiters and portal ranking": (Recruiters_portals_page, job_market_ratings),
        "UnderMinimum": (under_min_salary_page, under_minimum),
        "Story": story_page
    }

    selection = st.sidebar.radio("Page Menu", page_functions.keys())

    if selection == "Story":
        story_page()
    else:
        page_function, data_to_use = page_functions[selection]
        page_function(data_to_use)


if __name__ == "__main__":
    main()
