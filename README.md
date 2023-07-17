# sqlalchemy-challenge

**##PART 1: Task**

**##Precipitation Analysis**
In this task i used Python and SQLAlchemy to do a basic climate analysis and data exploration of climate database provided. Specifically, using SQLAlchemy ORM queries, Pandas, and Matplotlib.
**Requirements:**
Find the most recent date in the dataset.
Using that date, get the previous 12 months of precipitation data by querying the previous 12 months of data.
Select only the "date" and "prcp" values.
Load the query results into a Pandas DataFrame. Explicitly set the column names.
Sort the DataFrame values by "date".
Plot the results by using the DataFrame plot method, as the following image shows:

**##Station Analysis**
**Requirements:**
Design a query to calculate the total number of stations in the dataset.
Design a query to find the most-active stations (that is, the stations that have the most rows). To do so, complete the following steps:
List the stations and observation counts in descending order.

**Answered this  question:**  which station id has the greatest number of observations?
Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query
Design a query to get the previous 12 months of temperature observation (TOBS) data. Did this by completing the following steps:
Filter by the station that has the greatest number of observations.
Query the previous 12 months of TOBS data for that station.
Plot the results as a histogram.

**##Part 2: Designed the Climate App using Flask application**
