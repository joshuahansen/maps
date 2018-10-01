
from __future__ import print_function
from datetime import datetime
from datetime import timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

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
    calendarName = input("What would you like to call the calendar?")
    timezone = "Australia/Melbourne"

    created_calendar = add_calendar(calendarName, timezone)
     
    print(created_calendar['id'])

def add_calendar(calendarName, timezone):
    calendar = {
        "kind": "calendar#calendar",
        "summary": calendarName,
        "timeZone": timezone,
    }
    created_calendar = service.calendars().insert(body=calendar).execute()

    return created_calendar

if __name__ == '__main__':
    main()
