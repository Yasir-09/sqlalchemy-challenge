# Import the dependencies.

import numpy as np


from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Starter_Code\Resources\hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Base.classes.keys()
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs1<br/>"
        f"/api/v1.0/start_date_temp_stats/<start><br/>"
        f"/api/v1.0/between_start_&_end_dates_stats/<start>/<end><br/>"
        f"<b>IMPORTANT</b>: for /api/v1.0/<start><br/> the 'start date' uses the  format: YYYY-mm-dd <br/>"
        f"<b>IMPOIRTANT</b>: for /api/v1.0/<start>/<end><br/> use the following format to search between the 'Begin and End dates': YYYY-mm-dd/YYYY-mm-dd"
    )

#Create API for precipitation within last 12 months
@app.route("/api/v1.0/precipitation")
def precipitation():
   # Query precipitation analysis from the last 12 months
    one_year_back = print(dt.date(2017,8,23) - dt.timedelta(days= 365))

    one_year_back_date=dt.datetime(2016, 8, 22)

# # Perform a query to retrieve the data and precipitation scores
    one_year_data =  session.query(measurement.date, measurement.prcp).filter(measurement.date > one_year_back_date).all()  ## this returned a list of tuples from Select date and prcp columns from 
#measurement tables which is greater than a particular date ( eg > 1.1.2023)
    session.close()
    print(one_year_data)
#result : [('2016-08-24', 0.08), ('2016-08-25', 0.08), ('2016-08-26', 0.0), ('2016-08-27', 0.0), ('2016-08-28', 0.01), ('2016-08-29', 0.0), ('2016-08-30', 0.0), ('2016-08-31', 0.13)]

# Create a dictionaries containing precipitation and dates within the last 12 months of available data appending it to a list 
    data_list = []
    for data in one_year_data:
        data_dict = {}
        data_dict["Date"] = data[0]
        data_dict["PRCP"] = data[1]
        data_list.append(data_dict)

    return jsonify(data_list) 


#Create API for all the stations in the dataset
@app.route("/api/v1.0/stations") 

def stations():
    """Return a JSON list of stations from the dataset."""
    # Query all stations
    station_list = session.query(station.station, station.name).all()
    # stnt_list = list(np.ravel(station_list))
    session.close()

# # Creating a list of dictionaries from the list
    data_list = []
    for data in station_list:
        data_dict = {}
        data_dict["Station NO "] = data[0]
        data_dict["Station Name"] = data[1]
        data_list.append(data_dict)
    return jsonify(data_list)

#Create API for temperatures measured within the last 12 months of available data of the most popular station "USC00519281"
@app.route("/api/v1.0/tobs1")

def temperatures1():
    one_year_back_date=dt.datetime(2016, 8, 22)

    active_station = session.query(measurement.station, func.count(measurement.tobs)).group_by(measurement.station).order_by(func.count(measurement.tobs).desc()).all()
# active_station
    most_active_station = active_station[0]
    print(most_active_station[0])
    most_active_station_temp = session.query(measurement.date, measurement.tobs).filter(measurement.date > one_year_back_date, measurement.station == most_active_station[0]).all()
    most_active_station_temp
    session.close()
# Return a JSON list of temperatures, and dates from the dataset.

    data_list = []
    for data in most_active_station_temp:
        data_dict = {}
        data_dict["DATE "] = data[0]
        data_dict["Temperature "] = data[1]
        data_list.append(data_dict)
    return jsonify(data_list)
    
    
# Create an API route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

@app.route("/api/v1.0/start_date_temp_stats/<start>")
def begin_date(start):
    session = Session(engine)
    begin_date_results= session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()

    session.close()

# Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    data_list = []
    for data in begin_date_results:
        data_dict = {}
        data_dict["Min "] = data[0]
        data_dict["Average "] = data[1]
        data_dict["Max"]= data[2]
        data_list.append(data_dict)

    return jsonify(data_list)

# Create a route that when given the start date and end date, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user
@app.route("/api/v1.0/between_start_&_end_dates_stats/<start>/<end>")

def Start_end_date(start,end):
    session= Session(engine)
    start_end_date_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end ).all()

    session.close()

# Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    data_list = []
    for data in start_end_date_results:
        data_dict = {}
        data_dict["Min "] = data[0]
        data_dict["Average "] = data[1]
        data_dict["Max"]= data[2]
        data_list.append(data_dict)

        return jsonify(data_list)
    
if __name__ == '__main__':
    app.run(debug=True)