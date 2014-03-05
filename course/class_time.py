from datetime import datetime
from datetime import time as TM

class Time_Interval: 
    def __str__(self):
        if self.time_raw != 'TBA':
            return self.time_raw
        else:
            return 'TBA'
    def __eq__(self, other):
        return self.time_raw == other.time_raw
    def __ne__(self, other):
        return self.time_raw != other.time_raw
    def __unicode__(self):
        if self.time_raw != 'TBA':
            return self.time_raw + u''
        else:
            return 'TBA' + u''
    def __init__(self, time_raw):
        if time_raw != 'TBA':
            self.time_raw = time_raw
            start_raw, end_raw = time_raw.split(' - ')
            self.start_time = Class_Time(start_raw)
            self.end_time = Class_Time(end_raw)
        else:
            self.time_raw = time_raw
            self.start_time = Class_Time('11:00 pm')
            self.end_time = Class_Time('11:30 pm')

class Class_Time(TM):
    def __new__(self, time_raw):
        return datetime.strptime(time_raw, '%I:%M %p').time()
