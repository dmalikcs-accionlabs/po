import re
from builtins import len
from collections import namedtuple

s = '''
 

So to get Production ID we need:


Venue Name: Barclays Center
Can be provided by BSE
PrimaryPerformer: Blink 182
Can be provided by BSE
EventDate: 9/20/19
Can be provided by BSE
EventTime: 8:00 PM
Can be provided by BSE
ProductionID: 2701379
Can be looked up off of the 4 above pieces of information
 
'''


class ParserEmailBody:

    def __init__(self, body, debug=False):
        Event = namedtuple('Event', ('venue', 'date', 'time'))
        self.body = body
        self.debug = debug
        self.event_venue = None
        self.event_time = None
        self.event_date = None
        self._get_venue_name()
        self._get_event_time()
        self._get_event_date()
        self.event = Event(self.event_venue, self.event_date, self.event_time)

    def _get_venue_name(self):
        venue_names = re.findall('Venue\s*name\s*.*', self.body, re.IGNORECASE)
        if len(venue_names) == 1:
            for v in venue_names:
                n = re.sub(' +', ' ', v)
                match = re.search(":(.*)", n, re.IGNORECASE)
                if match and len(match.groups()) == 1:
                    venue = match.groups()[0]
                    self.event_venue = venue.strip()

    def _get_event_time(self):
        event_times = re.findall(r'event\s*time\s*(.*)', self.body, re.IGNORECASE)
        if len(event_times) == 1:
            for v in event_times:
                n = re.sub(' +', ' ', v)
                if self.debug: print(n)
                match = re.search(r"(\d{1,2}:\d{1,2}\s*(AM|PM))", n, re.IGNORECASE)
                if self.debug: print(match)
                if match and len(match.groups()) >= 1:
                    e_time = match.groups()[0]
                    self.event_time = e_time.strip()

    def _get_event_date(self):
        event_dates = re.findall(r'event\s*date\s*.*', self.body, re.IGNORECASE)
        if len(event_dates) == 1:
            for v in event_dates:
                n = re.sub(' +', ' ', v)
                match = re.search(r"\d{1,2}/\d{2}/\d{1,4}", n, re.IGNORECASE)
                if match:
                    self.event_date = match.group()


if __name__ == '__main__':
    p = ParserEmailBody(s)
    p._get_event_date()
    p._get_venue_name()
    p._get_event_time()
    print(p.event)
