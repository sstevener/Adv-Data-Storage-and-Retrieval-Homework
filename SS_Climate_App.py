from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, and_, desc, func

import pandas as pd

import numpy as np

import datetime 

from flask import Flask, jsonify

# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return(
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/start_date<br/>'
        f'/api/v1.0/start_date/end_date<br/>'
    )

# Query the dates and precipitation observations from the last year
# Return the JSON represenation the dictionary
@app.route('/api/v1.0/precipitation')
def precipitation():
    results = session.query(measurement.date, measurement.prcp)\
              .filter(measurement.date >= '2016-08-23').all()
    precipitation = {date: prcp for date, prcp in results}

    return jsonify(precipitation)    

# Return a JSON list of stations from the dataset
@app.route('/api/v1.0/stations')
def stations():
    all_stations = session.query(Station.station).all()

    return jsonify(all_stations)

# Query the dates and Temperature observations from the last 12 months of the dataset
# Return a JSON list of Temperature Observations (tobs) from the previous year
@app.route('/api/v1.0/tobs')
def tobs():
    end_date = session.query(measurement.date)\
    .order_by(measurement.date.desc()).first()

    end_date = end_date[0]

    previous_year = dt.datetime.strptime(end_date, "%Y-%m-%d")- dt.timedelta(days=365)

    yearly_temperature = session.query(measurement.date, measurement.tobs)\
    .filter(measurement.date >= previous_year).all()
    
    return jsonify(yearly_temperature)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route('/api/v1.0/<start>')
def start_only (start):
    start_only = session.query(func.min(Measurement.tobs),
    func.avg(Measurement.tobs),
    func.max(Measurement.tobs))\
    .filter(Measurement.date >= start).all()
        
    return jsonify(start_only)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
@app.route('/api/v1.0/<start>/<end>')
def start_end (start, end):
    start_end = session.query(func.min(Measurement.tobs),
    func.avg(Measurement.tobs),
    func.max(Measurement.tobs))\
    .filter(Measurement.date >= start)\
    .filter(Measurement.date <= end).all()
    
    return jsonify(start_end)

if __name__ == '__main__':
    app.run(debug=True)




















