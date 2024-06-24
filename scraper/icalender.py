from datetime import datetime, timedelta, timezone
from ics import Calendar
import requests

from ..helper import helper_time

class iCalender(Calendar):
    def __init__(self, url=None):
        super().__init__(url)

    def get_calendars_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            self.cal = Calendar(f.read())

    def get_calendars_from_url(self, url):
        self.cal = Calendar(requests.get(url).content.decode('utf-8'))
    
    def get_events(self):
        return self.cal.events

    def get_events_by_range(self, start_time=None, end_time=None):
        if type(start_time) != datetime or type(end_time) != datetime:
            raise ValueError('start_time and end_time must be datetime')
        if start_time > end_time:
            raise ValueError('start_time must be less than end_time')
        events = []
        for event in self.cal.events:
            if (event.begin.datetime >= start_time or start_time == None) and (event.end.datetime <= end_time or end_time == None):
                events.append(event)
        return events

    def get_today_events(self):
        events = []
        today = helper_time.now().date()
        for event in self.cal.events:
            if event.begin.datetime.year == today.year and event.begin.datetime.month == today.month and event.begin.datetime.day == today.day:
                events.append(event)
        return events

    def get_next_events(self, num=1):
        if type(num) != int:
            raise ValueError('num must be int')
        events = []
        now = helper_time.now()
        for event in self.cal.events:
            if event.begin.datetime >= now:
                events.append(event)
                num -= 1
            if num == 0:
                break
        return events