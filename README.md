This project involved analyzing and exploring climate data from a SQLite database using Python, SQLAlchemy, Pandas, and Matplotlib. 
The anlalysis includes precipitation data, temperature data, stations data, and the results are visualized using Matplotlib. The 
app.py file includes a Flask API which provides access to the data through a few different end points. Part 1 of the analysis is included 
in the climate_starter.ipynb file. The code goes through 5 steps. 1) Identifies the most recent date. 2) Uses that date to go back 1 year. 3) Queries 
the last 12 months of data and loads the results into a Pandas dataframe. 4) Sorts the data by date and provides visualization
using Matplotlib. 5) Calculates summary statistics for the temperature over the last 12 months with a second visualization. The next part 
of code in the climate_starter.ipynb file calculates the number of stations in the dataset. It then identifies the most active station,
and analyzes the temperature data for that station. Finally, we have a histogram that displays the most recent 12 months in the data.

The app.py file contains code for an API to serve the analyzed data. "/" displays the routes that are available. "/api/v1.0/precipitation" returns
a JSON object with precipitation data for the last 12 months which is sorted by date. "/api/v1.0/stations returns a JSON list of all 9 stations.
"/api/v1.0/tobs returns a JSON list of temperature observations for the most active station over the last 12 monts. 
"api/v1.0/<start>" returns a JSON list of the minimum, average, and maximum temperatures in a range beginning on the date until the end of the data.
<start> in the format yyyy-mm-dd. "/api/v1.0/<start>/<end>" returns a JSON list of the minimum, average, and maximum temperatures for 
the dates in that range. /<start>/<end> in the format yyyy-mm-dd/yyyy-mm-dd.
