from flask import Flask, request
from EventLogger import EventLogger
import json
import Helpers

#Create a Flask app instance
app = Flask(__name__)

#MySQL configuration
mysql_config = Helpers.read_json_from_file("config/mysql_config.json")


#Create an event logger instance
event_logger = EventLogger(mysql_config["host"], mysql_config["username"], mysql_config["password"], mysql_config["database"])

#Create the `log_event` route
@app.route("/log_event", methods=["POST"])
def log_event():
    return event_logger.log_event( request.form["event_type"], request.form["data"] )


#Create the get event
@app.route("/get", methods=["GET"])
def get():
    params = json.loads( request.args["params"] )

    if len(params) == 0:
        return event_logger.get( request.args["query"] )
        
    return event_logger.get( request.args["query"], json.loads( request.args["params"] ) )
