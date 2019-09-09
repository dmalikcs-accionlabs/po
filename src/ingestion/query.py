
class ProductionIdQuery:

    SELECT_PRODUCTION_ID_1 = '''SELECT	p.ProductionID
                                FROM	EIBoxOffice..Production p INNER JOIN  EIBoxOffice..Venue v ON p.VenueID = v.VenueID
                                WHERE	v.VenueName = '{}'
                                AND		p.EventDate = '{}' AND p.EventTime = '{}'
                                AND		p.Redirect = 1
                                AND   p.TM_Event_ID IS NOT NULL
                                '''
    SELECT_PRODUCTION_ID_2 = '''SELECT	p.ProductionID
                                FROM	EIBoxOffice..Production p
                                INNER JOIN  EIBoxOffice..Venue v ON p.VenueID = v.VenueID
                                WHERE	v.VenueName = '{}'
                                AND		p.EventDate = '{}'
                                AND   p.EventTime = '{}'
                                AND		p.Redirect = 1
                                '''
    SELECT_PRODUCTION_ID_3= '''SELECT	p.ProductionID
                                FROM	EIBoxOffice..Production p
                                INNER JOIN  EIBoxOffice..Venue v ON p.VenueID = v.VenueID
                                WHERE	v.VenueName = '{}'
                                AND		p.EventDate = '{}'
                                AND   p.EventTime = '{}'
                                '''

class ClientIdQery:

    SELECT_CLIENT_ID = '''SELECT ClientID FROM EIBoxOffice..Client WHERE CompanyName LIKE '{}' ; '''
