from flask import Flask, request
from EventLogger import EventLogger
import json

#Create a Flask app instance
app = Flask(__name__)

#MySQL configuration
host = "host"
username = "highlow"
password = "highlow"
database = "highlow"

#Create an event logger instance
event_logger = EventLogger(host, username, password, database)

#Create the `log_event` route
@app.route("/log_event", methods=["POST"])
def log_event():
    return event_logger.log_event( request.form["event_type"], request.form["data"] )


#Create the get event
@app.route("/get", methods=["GET"])
def get():
    return event_logger.get( request.args["query"], json.loads( request.args["params"] ) )
