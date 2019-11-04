# import dependencies

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect database
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"For start date queries: /api/v1.0/yyyy-mm-dd<br/>"
        f"For start and end date quereies: /api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation recorded for the last year [dates as determined in part 1]"""
    # Query 

    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Create dictionary
    precip = []
    for date, prcp in data:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip.append(precip_dict)

    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    stations = session.query(Station.station, Station.name).all()

    session.close()

    # Create dictionary
    station_list = []
    for station, name in stations:
        station_dict = {}
        station_dict["Station ID"] = station
        station_dict["Station Name"] = name
        station_list.append(station_dict)


    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature observations for the most active station for the last year [dates and station as determined in part 1]"""
    # Query most active stations
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
        filter_by(station = 'USC00519281').order_by(Measurement.date).all()

    session.close()

    # Create dictionary
    tob_list = []
    for date, tobs in temps:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Observed Temperature"] = tobs
        tob_list.append(tobs_dict)


    return jsonify(tob_list)

@app.route("/api/v1.0/<start_date>")
def start_date(start_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the temp min, max, and average for all observations after the given date"""
    # Query tobs
    results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()

    session.close()

    # Create dictionary
    results_list = []
    for result in results:
        results_dict = {}
        results_dict["Average Temp"] = result[0]
        results_dict["Maximum Temp"] = result[1]
        results_dict["Minimum Temp"] = result[2]
        results_list.append(results_dict)


    return jsonify(results_list)

@app.route("/api/v1.0/<start_date>/<end_date>")
def dates(start_date, end_date):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the temp min, max, and average for observations between the given dates"""
    # Query tobs
    date_results = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    # Create dictionary
    date_results_list = []
    for result in date_results:
        results_dict = {}
        results_dict["Average Temp"] = result[0]
        results_dict["Maximum Temp"] = result[1]
        results_dict["Minimum Temp"] = result[2]
        date_results_list.append(results_dict)


    return jsonify(date_results_list)

if __name__ == '__main__':
    app.run(debug=True)
