# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session= Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Climate API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data as JSON."""
    
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date_dt = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    start_date = most_recent_date_dt - dt.timedelta(days=365)

    results = session.query(Measurement.date, Measurement.prcp).filter(
        Measurement.date >= start_date).order_by(Measurement.date).all()
    
    
    # Convert query results to a dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""

    results = session.query(Station.station).all()
    station_list = [station[0] for station in results]

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature observations of the most active station for the previous year."""

    station_id = 'USC00519281'
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    most_recent_date_dt = dt.datetime.strptime(most_recent_date, "%Y-%m-%d")
    start_date = most_recent_date_dt - dt.timedelta(days=365)
    results = (
        session.query(Measurement.date, Measurement.tobs)
        .filter(Measurement.station == station_id)
        .filter(Measurement.date >= start_date)
        .order_by(Measurement.date)
        .all()
    )
    tobs_data = [{"date": date, "tobs": tobs} for date, tobs in results]
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start, end=None):
    """Return TMIN, TAVG, and TMAX for a specified date range."""
    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d")
        end_date = dt.datetime.strptime(end, "%Y-%m-%d") if end else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400


    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d") if end else None

    if end_date:
        results = (
            session.query(
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)
            )
            .filter(Measurement.date >= start_date)
            .filter(Measurement.date <= end_date)
            .all()
        )
    else:
        results = (
            session.query(
                func.min(Measurement.tobs),
                func.avg(Measurement.tobs),
                func.max(Measurement.tobs)
            )
            .filter(Measurement.date >= start_date)
            .all()
        )
    stats_data = {
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(stats_data)
session.close()

if __name__ == '__main__':
    app.run(debug=True)
    


