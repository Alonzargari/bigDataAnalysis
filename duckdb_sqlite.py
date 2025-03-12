# ---------------- Big Data: Last Exercise-----------------------
# Submitting:
# Re'em Hoisman
# Alon Zargari

"""
Here we run our queries on the data set and load the tables into duckdb
and copy the small data sets into sqlite file
"""

import duckdb
import os

# Create a connection to an DuckDB database in memory
connection = duckdb.connect("db_file.duckdb")
connection.execute("""
    CREATE TABLE IF NOT EXISTS JobsData AS
    SELECT * FROM read_csv_auto('job_descriptions.csv')
""")

# create sample 500 rows tables out of our original JobsData
connection.execute(
    """
    CREATE TABLE IF NOT EXISTS SampleJobsData AS
    SELECT * FROM JobsData USING SAMPLE 500;
    """
)

# -------------- duckdbToSqlite--------------
def duckdbToSqlite():
    """
    this function creates the sqlite "small" database file
    insert into it the relevant tables.
    more details on the queries and commend in the docs file
    """
    connection.execute("""
    ATTACH 'db_file.sqlite' AS sqlite_db (TYPE SQLITE);
    CREATE TABLE sqlite_db.SampleJobsData AS SELECT * FROM SampleJobsData;
    CREATE TABLE sqlite_db.TopCountriesJobPosts AS SELECT * FROM TopCountriesJobPosts ;
    CREATE TABLE sqlite_db.MinimumExperience AS SELECT * FROM MinimumExperience;
    CREATE TABLE sqlite_db.Discrimination AS SELECT * FROM Discrimination ;
    CREATE TABLE sqlite_db.JobMarketRatings AS SELECT * FROM JobMarketRating;
    CREATE TABLE sqlite_db.UnderMinimum AS SELECT * FROM UnderMinimum;
    """)


# -------------- saveTablesInDuckDB--------------
def saveTablesInDuckDB(tableName, query):
    """
    :param tableName: the name of the table we want to create
    :param query: the query that extract the relevant raws and cols from the JobsData table
    """
    createTable = "CREATE OR REPLACE TABLE " + tableName + " AS "
    connection.execute(createTable + query)
    result = connection.execute(f"SELECT * FROM {tableName}").fetchdf()
    print(result)


# -------------- CountryJobs table query--------------
query1 = """
WITH CompanyJobCount AS (
    SELECT Company, Country, COUNT("Job Id") AS Job_Count
    FROM JobsData
    WHERE Country IN ('Israel', 'USA', 'Japan', 'Germany', 'UK', 'France', 'Italy', 'Canada')
    GROUP BY Company, Country
)
SELECT Company,Country,Job_Count,
       ROW_NUMBER() OVER (PARTITION BY Country ORDER BY Job_Count DESC) AS Rank,
       CAST(SUM(Job_Count) OVER (PARTITION BY Country) AS INTEGER) AS Total_Jobs
FROM CompanyJobCount
QUALIFY
    Rank <= 5
ORDER BY Country, Rank
"""
# -------------- WorkType table query--------------
query2 = """
WITH JobsCount AS (
    SELECT
        CAST(str_split(Experience, ' to ')[1] AS INT) AS Min_experience,
        EXTRACT(YEAR FROM "Job Posting Date") AS Year,
        Qualifications,
        COUNT(*) AS Filtered_count
    FROM JobsData
    GROUP BY year, min_experience, Qualifications
)
SELECT Year, Min_experience, Qualifications, Filtered_count AS Job_count
FROM JobsCount
WHERE Min_experience IN (0, 1, 2) 
ORDER BY Year, Qualifications, Min_experience;
"""

# -------------- Discrimination table query--------------
query3 = """
SELECT Qualifications, Preference, Country, COUNT(*) AS Job_Count
FROM JobsData
GROUP BY Qualifications, Preference, Country 
ORDER BY Country, Qualifications, Preference
"""

# -------------- JobMarketRating table query--------------
query4 = """
WITH RecruiterRankings AS (
    SELECT "Job Portal" AS Portal, "Contact Person" AS Contact_Person,
            ROW_NUMBER() OVER (PARTITION BY Portal ORDER BY COUNT(*) DESC) AS Recruiter_Rank
    FROM JobsData
    GROUP BY Portal, Contact_Person
    QUALIFY
        Recruiter_Rank <= 3
),
PortalRankings AS (
    SELECT "Job Portal" AS Portal, COUNT(*) AS Job_Posts, 
    RANK() OVER (ORDER BY Job_Posts DESC) as Portal_Rank
    FROM JobsData
    GROUP BY Portal
    QUALIFY
        Portal_Rank <= 5
)
SELECT Portal, Job_Posts, Portal_Rank, Contact_Person, Recruiter_Rank
FROM PortalRankings AS pr
JOIN RecruiterRankings
USING (Portal)
ORDER BY Portal_Rank, Recruiter_Rank
"""

# -------------- UnderMinimum table query--------------
query5 = """
WITH SplitSalary AS (
    SELECT Company,
           CAST(SPLIT_PART(REPLACE(REPLACE("Salary Range", '$', ''), 'K', ''), '-', 1) AS INTEGER) * 1000 AS Min_Salary
    FROM JobsData
),
MarketAverage AS (
    SELECT AVG(Min_Salary) AS Market_Avg_Salary
    FROM SplitSalary
)
SELECT s.Company, COUNT(*) AS Below_Avg
FROM SplitSalary s
CROSS JOIN MarketAverage m
WHERE s.Min_Salary < m.Market_Avg_Salary
GROUP BY s.Company
ORDER BY Below_Avg DESC
"""

# ----------------------------------------------------
# Calling the function that create the table from the query
saveTablesInDuckDB("TopCountriesJobPosts", query1)
saveTablesInDuckDB("MinimumExperience", query2)
saveTablesInDuckDB("Discrimination", query3)
saveTablesInDuckDB("JobMarketRating", query4)
saveTablesInDuckDB("UnderMinimum", query5)

# only if we did not load the tables to Sqlite yet
if not os.path.exists("db_file.sqlite"):
    duckdbToSqlite()

connection.close()
