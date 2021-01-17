from __future__ import print_function
import datetime
import pytz
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def formatTime(start_timezone, start_time, end_time, recur_end_date=None):
    """
    Formats the timing based on the API requirements.

    :param start_time: datetime object (Y, m, D, H, M)
    :param start_timezone: string local timezone of user (format Continent/City)
    :param end_time: datetime object (Y, m, D, H, M)
    :param recur_end_date: datetime object (Y, m, D, H, M)
    :return:
    """
    if(start_time.tzinfo is None):
        timezone = datetime.timedelta(hours=float(start_timezone), minutes=0)
        start_time = start_time + timezone
    start_time = start_time.astimezone(pytz.timezone('UTC'))
    start_time = datetime.datetime.strftime(start_time, "%Y-%m-%dT%H:%M:%SZ")

    if(end_time.tzinfo is None):
        timezone = datetime.timedelta(hours=float(start_timezone), minutes=0)
        end_time = end_time + timezone
    end_time = end_time.astimezone(pytz.timezone('UTC'))
    end_time = datetime.datetime.strftime(end_time, "%Y-%m-%dT%H:%M:%SZ")

    if recur_end_date is not None:
        timezone = datetime.timedelta(hours=float(start_timezone), minutes=0)
        recur_end_date = recur_end_date + timezone
        recur_end_date = recur_end_date.astimezone(pytz.timezone('UTC'))
        recur_end_date = datetime.datetime.strftime(recur_end_date, "%Y%m%dT%H%M%SZ")

    return start_time, end_time, recur_end_date 

def createEvent(event_title, timezone, start_time, end_time, recur_end_date=None, recur_freq=None):
    """
    Create a google event dictionary. Sets a default reminder

    All params are string type.
    :param event_title: Name of the event
    :param start_time: start time of event (format '2021-05-28T09:00:00-07:00')
    :param timezone: timezone of start time (Country_Name/City)
    :param end_time: end time of event (format '2021-05-28T17:00:00-07:00')
    :param recur_freq: how frequently will the event recur (DAILY, WEEKLY)
    :param recur_end_date: when will the event recurrence stop (format 20110617T065959Z)
    :return: event dictionary
    """

    if recur_freq is not None:
        event = {
            'summary': event_title,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            },
            'recurrence': [
                'RRULE:FREQ={};UNTIL={}'.format(recur_freq, recur_end_date)
            ],
            'reminders': {
                'useDefault': True
            },
        }
    else:
        event = {
            'summary': event_title,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            },
            'reminders': {
                'useDefault': True
            },
        }

    return event


def master(event_title, curr_timezone, req_timezone, start_date, end_time, end_date, freq, http_auth):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    service = build('calendar', 'v3', http_auth)

    start_time, end_time, recur_end_date = formatTime(
        curr_timezone,
        start_date,
        end_time,
        end_date)

    timezone = 'GMT'
    if '-' not in req_timezone:
        req_timezone = '+' + req_timezone
    else:
        req_timezone = timezone + req_timezone

    event = createEvent(event_title=event_title,
                        timezone=req_timezone,
                        start_time=start_time,
                        end_time=end_time,
                        recur_end_date=recur_end_date,
                        recur_freq=freq)

    event = service.events().insert(calendarId='primary', body=event).execute()
    # print('Event created: %s' % (event.get('htmlLink')))
    return event.get('htmlLink')


if __name__ == '__main__':
    master('Google', 'America/Toronto', '-2', datetime.datetime(2021, 1, 17, 9, 30),
           datetime.datetime(2021, 1, 17, 10, 30), datetime.datetime(2021, 4, 18, 10, 30), 'WEEKLY')



