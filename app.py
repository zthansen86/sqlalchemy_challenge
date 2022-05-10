# 1. import Flask
from asyncio import start_server
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)




# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
#Prints message in terminal
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list 
    precip_data = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_data.append(precip_dict)

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    """Return a list of all station names"""
    # Query all passengers
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= query_date).filter(Measurement.station == "USC00519281").all()

    session.close()

    tobs_data = list(np.ravel(results))
    
    return jsonify(tobs_data)


## 2016%2D08%2D23 for dash
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def start_date(start, end = None):
    """Fetch the start date from
       the path variable supplied by the user, or a 404 if not."""
    session = Session(engine)
    sel = [func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
        tobs_data = list(np.ravel(results))
        return jsonify(tobs_data)        
    else:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
        tobs_data = list(np.ravel(results))
        return jsonify(tobs_data)

    session.close()



if __name__ == "__main__":
    app.run(debug=True)