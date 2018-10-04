
from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

import configparser
import MySQLdb.cursors
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from datetime import timedelta
from app.database_tables.patient import Doctor


config = configparser.ConfigParser()
config.read('../config.ini')

if 'gcpMySQL' in config:
    HOST = config['gcpMySQL']['host']
    USER = config['gcpMySQL']['user']
    PASS = config['gcpMySQL']['pass']
    DBNAME = config['gcpMySQL']['db']

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{}:{}@{}/{}'.format(USER,PASS,HOST,DBNAME)

db = SQLAlchemy(app)
ma = Marshmallow(app)

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('../token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('../credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    print("Please enter new doctors details below")
    fname = input("Enter First Name: ")
    lname = input("Enter Last Name: ")
    email = input("Enter email address: ")
    calendarName = input("What would you like to call the calendar?")

    timezone = "Australia/Melbourne"

    created_calendar = add_calendar(calendarName, timezone)
     
    print(created_calendar['id'])

    add_doctor(fname, lname, email, created_calendar['id'])

def add_calendar(calendarName, timezone):
    calendar = {
        "kind": "calendar#calendar",
        "summary": calendarName,
        "timeZone": timezone,
    }
    created_calendar = service.calendars().insert(body=calendar).execute()

    return created_calendar

def add_doctor(firstname, lastname, email, calendarID):
    new_doctor = Doctor(firstname, lastname, email, calendarID)

    db.session.add(new_doctor)
    db.session.commit()
    

if __name__ == '__main__':
    main()
