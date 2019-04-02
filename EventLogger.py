import pymysql
import bleach
import json
import datetime



class EventLogger:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

        self.queries = {}

        with open("queries.json", "r") as query_file:
            queries_string = query_file.read()

            #Load the JSON
            self.queries = json.loads(queries_string)

    def log_event(self, event_type, data):
        #Clean the type and the data
        event_type = bleach.clean(event_type)
        data = bleach.clean( json.dumps(data) )

        #Get the timestamp
        timestamp = datetime.datetime.now().timestamp()

        #Connect to MySQL database
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Insert a new row
        cursor.execute("INSERT INTO events(type, data, timestamp) VALUES('" + event_type + "', '" + data + "', " + timestamp + ");")

        #Commit and close the connection
        conn.commit()
        conn.close()

        return ""

    def get(self, query, params=[]):
        #Clean the parameters
        for i in range(params):
            params[i] = bleach.clean( params[i] )

        #Get the SQL statement for the query
        sql_statement = self.queries[query].format(*params)

        #Connect to MySQL database
        conn = pymysql.connect(self.host, self.username, self.password, self.database, cursorclass=pymysql.cursors.DictCursor)
        cursor = conn.cursor()

        #Get the appropriate data by executing the SQL statement
        cursor.execute(sql_statement)

        #Unpack the data
        data = cursor.fetchall()

        #Commit and close the connection
        conn.commit()
        conn.close()

        #Return the data
        return json.dumps(data)
