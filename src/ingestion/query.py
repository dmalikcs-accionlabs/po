from django.utils.decorators import classonlymethod
from emerald.lib.database import Database

class ProductionIdQuery:
    production_id = None
    is_many = None

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
        for q in self.get_queries():
            qr = q.format(venue, eventdate, eventtime)
            data = self.con.query(qr)
            if data:
                rows = data.fetchall()
                print(" Production Ids results : ", rows)
                if len(rows) == 1 and rows[0][0] is not None:
                    self.production_id = rows[0][0]
                    self.m_production_id = False
                    break;
                elif len(rows) >= 0:
                    self.m_production_id = True
                else:
                    pass



class ClientIdQuery:
    SELECT_CLIENT_ID = '''SELECT ClientID FROM EIBoxOffice..Client WHERE CompanyName LIKE '{}' ; '''

#
# # VENU_NAME = 'Scotiabank Arena'
# from ingestion.query import  ProductionIdQuery
# p = ProductionIdQuery()
# p.get_production_id('Scotiabank Arena','2009-12-07 00:00:00', '1900-01-01 19:00:00')