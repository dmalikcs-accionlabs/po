from builtins import isinstance

from emerald.lib.database import Database
from datetime import date, time


class ProductionIdQuery:
    EVENT_DATE_FORMAT = '%Y-%m-%d 00:00:00'
    EVENT_TIME_FORMAT = '1900-01-01  %H:%M:00'
    production_id = None
    is_many = None
    events = None

    GET_PRODUCTION_ID_QUERY1 = '''SELECT	p.ProductionID
                                FROM	EIBoxOffice..Production p INNER JOIN  EIBoxOffice..Venue v ON p.VenueID = v.VenueID
                                WHERE	v.VenueName = '{}'
                                AND		p.EventDate = '{}' 
                                AND     p.EventTime = '{}'
                                AND		p.Redirect = 1
                                AND     p.TM_Event_ID IS NOT NULL
                                '''
    GET_PRODUCTION_ID_QUERY2 = '''SELECT	p.ProductionID
                                FROM	EIBoxOffice..Production p
                                INNER JOIN  EIBoxOffice..Venue v ON p.VenueID = v.VenueID
                                WHERE	v.VenueName = '{}'
                                AND		p.EventDate = '{}'
                                AND     p.EventTime = '{}'
                                AND		p.Redirect = 1
                                '''
    GET_PRODUCTION_ID_QUERY3 = '''SELECT	p.ProductionID
                                FROM	EIBoxOffice..Production p
                                INNER JOIN  EIBoxOffice..Venue v ON p.VenueID = v.VenueID
                                WHERE	v.VenueName = '{}'
                                AND		p.EventDate = '{}'
                                AND   p.EventTime = '{}'
                                '''

    def __init__(self, *args, **kwargs):
        self.con = Database('monarch_replica')

    def get_queries(self):
        return (
            self.GET_PRODUCTION_ID_QUERY1,
            self.GET_PRODUCTION_ID_QUERY2,
            self.GET_PRODUCTION_ID_QUERY3
        )

    def get_production_id(self, venue, eventdate, eventtime):
        events = lambda rows: [{'production_id': row[0],
                                # 'event name': row[1],
                                # 'event date': row[2],
                                # 'event time': row[2],
                                # 'venue name': row[2],
                                # 'venue id': row[2],
                                }
                               for row in rows]

        if isinstance(eventdate, date) \
                and isinstance(eventtime, time):
            event_date = eventdate.strftime(self.EVENT_DATE_FORMAT)
            event_time = eventtime.strftime(self.EVENT_TIME_FORMAT)

        for q in self.get_queries():
            qr = q.format(venue, event_date, event_time)
            data = self.con.query(qr)
            if data:
                rows = data.fetchall()
                self.events = events(rows)
                print(" Production Ids results : ", rows)
        return self.events
                # if len(rows) == 1 and rows[0][0] is not None:
                #     self.events = events(rows)
                #     break;
                # elif len(rows) >= 1:
                # self.events = events(rows)
                # break;
                # else:
                #     pass


if __name__ == '__main__':
    # VENU_NAME = 'Scotiabank Arena'
    p = ProductionIdQuery()
    p.get_production_id('Scotiabank Arena', '2009-12-07', '7:00 PM')
    print(p.events)
