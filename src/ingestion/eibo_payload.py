class PreparePayload(object):

    def __init__(self, performer=None, venue=None, eventdate=None,
                 eventtime=None, vendor=None, isConsign=True, isCombined=True,
                 fee=None, primaryprovider='Ticketmaster'):
        self.vendor = vendor
        self.performer = performer
        self.venue = venue
        self.eventdate = eventdate
        self.eventtime = eventtime
        self.isConsign = isConsign
        self.isCombined = isCombined
        self.fee = fee
        self.primaryprovider = primaryprovider
        self.inventory_import_obj = {}
        self.conn_string = 'Driver={ODBC Driver 17 for SQL Server};Server=172.16.10.5;Database=DynastyApp;UID=DynastyTopaz;PWD=lo3FGlUNtdSq1rj3twO0;TrustServerCertificate=yes;Connection Timeout=120;'

    def select_vendorid(self, conn):
        from .query import ClientIdQery
        select_clientid = ClientIdQery.SELECT_CLIENT_ID
        with conn.cursor() as cur:
            print(" select_clientid query : ", select_clientid.format(self.vendor))
            cur.execute(select_clientid.format(self.vendor))
            result = cur.fetchall()
            print("Client Id result : ", result)
            if len(result) >= 1 and result[0][0] is not None:
                self.vendorid = result[0][0]
                print(" self.vendorid  : ", self.vendorid)
            else:
                raise ValueError('RowCount > 1')

    def select_productionid(self, conn, query):
        with conn.cursor() as cur:
            qr = query.format(self.venue, self.eventdate, self.eventtime)
            print(" Query : ", qr)
            cur.execute(qr)
            result = cur.fetchall()
            print(" Production Ids results : ", result)
            if len(result) == 1 and result[0][0] is not None:
                self.productionid = result[0][0]
            else:
                raise ValueError('RowCount > 1')

    def create_inventory_object(self, file_seatblocks, file_barcodes=None):
        import pyodbc
        import datetime
        import pandas as pd
        from .query import ProductionIdQuery

        file_name = f'{self.venue}_{self.performer}_import_{datetime.datetime.now().strftime("%m%d%y%#I%M%p")}'
        print("file_name  :  ", file_name)
        conn = pyodbc.connect(self.conn_string)
        try:
            self.select_vendorid(conn)
        except ValueError:
            print('ClientID not present in EiBo client table!')
            exit(1)
        try:
            self.select_productionid(conn, ProductionIdQuery.SELECT_PRODUCTION_ID_1.format(self.venue, self.eventdate, self.eventtime))
        except ValueError:
            try:
                self.select_productionid(conn, ProductionIdQuery.SELECT_PRODUCTION_ID_2.format(self.venue, self.eventdate, self.eventtime))
            except ValueError:
                try:
                    self.select_productionid(conn, ProductionIdQuery.SELECT_PRODUCTION_ID_3.format(self.venue, self.eventdate, self.eventtime))
                except ValueError:
                    print(
                        f'ProductionID could be not be isolated for {self.eventdate}! Please review after the process is complete.')
                    exit(1)
        conn.close()

        if file_seatblocks.endswith(('.xls', '.xlsx')):
            inventory_df = pd.read_excel(file_seatblocks, sheet_name=0)
        elif file_seatblocks.endswith('.csv'):
            inventory_df = pd.read_csv(file_seatblocks, delimiter=',')

        self.inventory_import_obj["bulkImport_BatchID"] = 0
        self.inventory_import_obj["importCompanyId"] = self.vendorid
        self.inventory_import_obj["type"] = 1
        self.inventory_import_obj["deliveryType"] = 1
        self.inventory_import_obj["isInHand"] = True
        self.inventory_import_obj["isConsign"] = self.isConsign
        self.inventory_import_obj["consignmentTerms"] = self.fee
        self.inventory_import_obj["seasonProductionIds"] = []
        self.inventory_import_obj["isSeason"] = False
        self.inventory_import_obj["fileName"] = file_name
        self.inventory_import_obj["importType"] = 1
        self.inventory_import_obj["listings"] = []
        for i, data in inventory_df.iterrows():
            print(" row data : ", data)
            listing_obj = {
                "listPriceEach": 5000.00,
                "section": str(data['section_name']),
                "row": str(data['row_name']),
                "startSeat": int(data['seat_num']),
                "endSeat": int(data['last_seat']),
                "quantity": int(data['num_seats']),
                "costEach": 0.0,
                "internalNote": None,
                "externalNote": None,
                "productionId": self.productionid,
                "eventDate": None,
                "eventTime": None,
                "eventCity": None,
                "barcodes": []
            }
            if file_barcodes is not None:
                barcode_df = pd.read_csv(file_barcodes, delimiter=',')
                barcode_df = barcode_df.applymap(str)
                for i in range(listing_obj["startSeat"], listing_obj["endSeat"] + 1):
                    listing_obj["barcodes"].append({
                        "seatNumber": i,
                        "barcode": barcode_df.loc[
                            (barcode_df["section_name"] == listing_obj["section"])
                            & (barcode_df["row_name"] == listing_obj["row"])
                            & (barcode_df["seat_num"] == str(i)),
                            "barcode"].values[0]
                    })
            self.inventory_import_obj['listings'].append(listing_obj)

        return self.inventory_import_obj