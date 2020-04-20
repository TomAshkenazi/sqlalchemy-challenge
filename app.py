import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/api/v1.0/precipitation")
def precip():

    """Return a list of dates and tobs"""
    """Query for the dates and temperature observations from the last year.
    Convert the query results to a Dictionary using date as the key and tobs as the value.
    Return the JSON representation of your dictionary."""

    print("Server recieved request for precip...")
    all_tobs = []
    results = session.query(Measurement).filter(Measurement.date > '2016-08-24').filter(Measurement.date <= '2017-08-23').all()
    for data in results:
        tobs_dict = {}
        tobs_dict[data.date] = data.tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/stations")
def stations():
    print("Server recieved request for STATIONS...")
    """Return a JSON list of stations from the dataset."""

    # Query all stations
    station_results = session.query(Station.station).all()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_results))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    print("Server recieved request for TOBS...")
    """Return a JSON list of Temperature Observations (tobs) for the previous year."""

    # Query all tobs
    tobs_results = session.query(Measurement.tobs).all()

    # Convert list of tuples into normal list
    tobs_list = list(np.ravel(tobs_results))

    return jsonify(tobs_list)


@app.route("/api/v1.0/<startdate>")
def tobs_by_date(startdate):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date."""

    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all())


@app.route("/api/v1.0/<startdate>/<enddate>")
def tobs_by_date_range(startdate, enddate):
    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
        When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive."""

    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all())


if __name__ == "__main__":
    app.run(debug=True)
