# Import the dependencies.

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(engine, reflect = True)

# View all of the classes that automap found
base.classes.keys()

# Save references to each table
measurement = base.classes.measurement
station = base.classes.station 

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def homepage():
    return (
        f"Welcome!<br/>"
        f"Available Routes:<br/>"
        f"//api/v1.0/percipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/percipitation") 
def precipitation():
    # Perform a query to retrieve the data and precipitation scores
    scores = session.query(measurement.date, measurement.prcp).filter(measurement.date>=prev_year).all()
    session.close()
    return jsonify(scores)
    
@app.route("/api/v1.0/stations")
def stations():
    # Design a query to calculate the total number of stations in the dataset
    session.query(func.count(station.station)).all()
    session.close()
    return jsonify(session)

@app.route("/api/v1.0/tobs")
def tobbs():
    # Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    tobs = session.query(measurement.tobs).filter(measurement.station == "USC00519281").\
    filter(measurement.date >= prev_year).all()
     session.close()
    return jsonify(tobbs)

@app.route("/api/v1.0/<start>")

@app.route("/api/v1.0/<start>/<end>")

if __name__ == '__main__':
    app.run(debug=True)