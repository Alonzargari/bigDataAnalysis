# ---------------- Big Data: Last Exercise-----------------------
# Submitting:
# Re'em Hoisman - 211694146
# Alon Zargari - 208626515

"""
This file aggregates multiple plotting functions designed to visualize job market data.
It provides various charts and visual representations to help users analyze query results
interactively within a Streamlit dashboard.
"""

import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
from wordcloud import WordCloud


def recruiters_portal_ranking_plots(df):

    """
    Generates a stem plot showing the number of job posts per portal,
    highlighting the top 3 recruiters for each.
    """

    portal_jobs = df.drop_duplicates('Portal')[['Portal', 'Job_Posts']]

    colors = ['red', 'blue', 'green']
    fig, ax = plt.subplots(figsize=(10, 8))
    markerline, stemlines, baseline = plt.stem(range(len(portal_jobs)), portal_jobs['Job_Posts'].values)
    plt.setp(baseline, color='k', linewidth=0.5)
    plt.setp(markerline, markersize=6)

    for i, (portal, jobs) in enumerate(zip(portal_jobs['Portal'], portal_jobs['Job_Posts'])):
        portal_recruiters = df[df['Portal'] == portal]['Contact_Person'].values[:3]

        plt.text(i, jobs + 1000, portal_recruiters[0], ha='center', va='bottom', color=colors[0])
        plt.text(i, jobs + 600, portal_recruiters[1], ha='center', va='bottom', color=colors[1])
        plt.text(i, jobs + 200, portal_recruiters[2], ha='center', va='bottom', color=colors[2])

    plt.xticks(range(len(portal_jobs)), portal_jobs['Portal'],  ha='right')

    plt.ylim(portal_jobs['Job_Posts'].min() * 0.95, portal_jobs['Job_Posts'].max() * 1.05)
    plt.xlim(-0.5, len(portal_jobs) - 0.5)
    plt.title('Job Posts by Portal with Top 3 Recruiters')
    plt.ylabel('Number of Job Posts')

    legend_elements = [
        plt.Line2D([0], [0], color=colors[0], label='Rank 1'),
        plt.Line2D([0], [0], color=colors[1], label='Rank 2'),
        plt.Line2D([0], [0], color=colors[2], label='Rank 3')
    ]
    plt.legend(handles=legend_elements, loc='upper right')
    _, col1, _ = st.columns([0.5, 2, 0.5])
    with col1:
        st.pyplot(fig)


def min_experience_plot(df):
    """
    Creates a bar chart displaying job counts by
    degree and year for a selected experience level, with interactive filters.
    """
    col1, _, col2 = st.columns([3, 0.2, 1])
    with col2:
        st.markdown("Filters:")
        selected_experience = st.selectbox('Select Experience Level:', sorted(df['Min_experience'].unique()), index=0)
        selected_years = st.multiselect('Select Years:', sorted(df['Year'].unique()),
                                        default=sorted(df['Year'].unique()))
        selected_degrees = st.multiselect('Select Qualifications:', sorted(df['Qualifications'].unique()),
                                          default=sorted(df['Qualifications'].unique()))

    with col1:
        filtered_df = df[(df['Year'].isin(selected_years)) & (df['Qualifications'].isin(selected_degrees)) & (
                df['Min_experience'] == selected_experience)]

        basic_colors = ['blue', 'red', 'orange', 'green', 'purple', 'cyan', 'magenta', 'lime', 'pink', 'gray']
        qualification_colors = {degree: basic_colors[i % len(basic_colors)] for i, degree in
                                enumerate(sorted(df['Qualifications'].unique()))}

        fig, ax = plt.subplots(figsize=(12, 6))
        positions = []
        labels = []
        added_labels = []
        for (degree, year), group in filtered_df.groupby(['Qualifications', 'Year']):
            position = f'{degree} {year}'
            positions.append(position)
            labels.append(f'{year}')
            job_count = group['Job_count'].sum()
            ax.bar(position, job_count, width=0.4, color=qualification_colors[degree],
                   label=degree if degree not in added_labels else "_nolegend_")
            added_labels.append(degree)

        ax.set_xlabel('Degree and Year')
        ax.set_ylabel('Job count')
        ax.set_title('Job count by degree and year for a specific experience level')
        ax.set_xticks(positions)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontweight='bold')
        if len(added_labels)>0:
            ax.legend()
        st.pyplot(fig)


def discrimination_posts_plot(df):

    """
    Visualizes job availability by country based on gender preferences and
    qualifications using an interactive choropleth map.
    """

    df['Job_Count'] = pd.to_numeric(df['Job_Count'], errors='coerce').fillna(0)
    col1_filter, col2_filter, col3_filter = st.columns(3)
    with col1_filter:
        selected_countries = st.selectbox(
            "Select Countries",
            options=df['Country'].unique(),
        )

    with col2_filter:
        selected_preferences = st.selectbox(
            "Select Gender Preferences",
            options=df['Preference'].unique(),
        )

    with col3_filter:
        selected_qualifications = st.multiselect(
            "Select Qualifications",
            options=df['Qualifications'].unique(),
        )

    filtered_df = df[
        (df['Country'] == selected_countries) &
        (df['Preference'] == selected_preferences) &
        df['Qualifications'].isin(selected_qualifications)
        ]
    country_gender_jobs_filtered = filtered_df.groupby('Country', as_index=False)['Job_Count'].mean()

    geo_fig = px.choropleth(
        country_gender_jobs_filtered,
        locations="Country",
        locationmode="country names",
        color="Job_Count",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        range_color=[0, 300],
        title="Job Availability by Country",
        labels={"Job_Count": "Number of Jobs"}
    )

    geo_fig.update_layout(
        geo=dict(showcoastlines=True, coastlinecolor="Black"),
        height=600
    )

    st.plotly_chart(geo_fig)
    st.write("Filtered Data:", filtered_df)


def under_min_salary_plot(df):
    """
    Generates a word cloud representing the distribution of job postings
     by companies offering salaries below the minimum threshold.
     """
    company_salary_counts = df['Company'].value_counts().to_dict()

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(company_salary_counts)

    fig = plt.figure(figsize=(12, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    _, col1, _ = st.columns([0.1, 2, 0.5])
    with col1:
        st.pyplot(fig)


def leading_countries_job_posts(df):
    """
    Displays a treemap of the top 5 companies per country based on job postings
    highlighting job distribution across leading countries.
    """
    _, col1, _ = st.columns([0.5,2,0.5])
    with col1:
        fig = px.treemap(df,
                         path=['Country', 'Company'],
                         values='Job_Count',
                         color='Total_Jobs',
                         hover_data=['Company', 'Total_Jobs'],
                         color_continuous_scale='Greens',
                         title="Top 5 Companies per Country - Treemap")
        st.plotly_chart(fig)
