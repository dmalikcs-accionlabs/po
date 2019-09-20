from emerald.celery import app
from celery import  Task
from .choices import StatusChoice, \
    TaskChoice
from django.core.serializers.json import DjangoJSONEncoder

import tablib
import magic
import time
import json


class ParseEmailBodyTask(Task):
    name = 'parse_email_body_task'

    def run(self, *args, **kwargs):
        from .models import IngestionData
        pk = args[0]
        i = IngestionData.objects.get(pk=pk)
        i.parse_email_body()
        return pk

    def on_success(self):
        pass

    def on_failure(self):
        pass


class FetchProductionTask(Task):

    def run(self, *args, **kwargs):
        from .models import IngestionData
        pk = args[0]
        i = IngestionData.objects.get(pk=pk)
        i.fetch_production_id()
        return pk

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


class SelectParserTask(Task):
    name = 'select_parser'

    def run(self, *args, **kwargs):
        from .models import IngestionData
        pk = args[0]
        i = IngestionData.objects.get(pk=pk)
        if not i.parser:
            raise Exception("Parser not defined")
        return {'ingestion_object': i}

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        from .models import IngestionData, \
            IngestionDataTask
        pk = args[0]
        i = IngestionData.objects.get(pk=pk)
        i.notes = 'No parser defined for user!'
        i.einfo = einfo
        i.status = StatusChoice.COMPLETED_FAILED
        i.save()
        IngestionDataTask.objects. \
            create(ingestion=i, task=TaskChoice.ACK, status=StatusChoice.STOPED, notes='Unable to find parser')


class ValidateFileFormatTask(Task):
    name = 'validate_file_format_task'

    def run(self, *args, **kwargs):
        from .models import IngestionData
        pk = args[0]
        i = IngestionData.objects.get(pk=pk)
        for attachment in i.get_attached_files():
            if magic.from_buffer(attachment.data_file.read(), mime=True) \
                    in ['application/vnd.ms-office', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', ]:
                return {
                    'ingestion_request_id': pk,
                    'file_id': attachment.pk
                }
            else:
                raise Exception('Unsupported file')

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.VALIDATE_FILE_FORMAT, notes="File Format is correct")

    def on_failure(self,  exc, task_id, args, kwargs, einfo):
        from .models import IngestionData
        pk = args[0]
        i = IngestionData.objects.get(pk=pk)
        i.status = StatusChoice.COMPLETED_FAILED
        i.save()


class ValidateColumnNameTask(Task):
    name = 'validate_column_name_task'

    def __init__(self, *args, **kwargs):
        super(ValidateColumnNameTask, self).__init__(*args, **kwargs)
        self.missing_column = []

    def run(self, *args, **kwargs):
        from .models import IngestionData, IngestionDataAttachment
        print("called Validated column name format")
        ret = args[0]
        i = IngestionData.objects.get(pk=ret['ingestion_request_id'])
        attached_file = IngestionDataAttachment.objects.get(pk=ret['file_id'])
        received_headers = [header.lower()
                            for header in self.get_received_headers(attached_file.data_file)
                            if isinstance(header, str)]
        applied_parser = None
        for parser in i.get_parsers():
            expected_headers = self.get_expected_headers(parser=parser)
            if expected_headers:
                applied_parser = parser
            for header in expected_headers:
                if not header.lower() in received_headers:
                    self.missing_column.append(header.lower())
                    applied_parser = None
                    #todo: logic need to change
                    break;
        if not applied_parser:
            raise Exception('No parser compatible')
        return ret


    def get_received_headers(self, file_name):
        dataset = tablib.Dataset()
        dataset.xls = file_name.read()
        return dataset.headers

    def get_expected_headers(self, parser):
        return parser.get_expected_columns()

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.VALIDATE_COLUMN_NAME)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        from .models import IngestionData, IngestionDataTask
        ret = args[0]
        i = IngestionData.objects.get(pk=ret['ingestion_request_id'])
        i.status = StatusChoice.COMPLETED_FAILED
        i.save()
        kw = {
            'ingestion':i,
            "status": StatusChoice.COMPLETED_FAILED,
            "task": TaskChoice.VALIDATE_COLUMN_NAME
        }
        if self.missing_column:
            notes = "{} columns are missing".format(','.join(self.missing_column))
            kw.update({'notes': notes})
        IngestionDataTask.objects.create(**kw)


class InventoryIngestionTask(Task):
    name = 'inventory_ingestion_task'

    def run(self, *args, **kwargs):
        from .models import IngestionData, IngestionDataTask
        time.sleep(2)
        ret = args[0]
        ingestion_obj = IngestionData.objects.get(pk=ret['ingestion_request_id'])
        for inventory in ingestion_obj.ingestion_inventories.all():
            pass
            #inventory.process()
        return ret

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.INGESTION_TASK, notes="Sub tasks created for all inventory")


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        from .models import IngestionData, IngestionDataTask
        ret = args[0]
        i = IngestionData.objects.get(pk=ret['ingestion_request_id'])
        i.status = StatusChoice.COMPLETED_FAILED
        i.save()
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_FAILED, task=TaskChoice.INGESTION_TASK, notes="Failed to create sub tasks")

class ValidateColumnDataTask(Task):
    name = 'validate_column_data_task'

    def run(self, *args, **kwargs):
        from .models import IngestionInventory
        inventory = args[0]
        inv_obj = IngestionInventory.objects.get(pk=inventory)
        return {'inventory_pk': inv_obj.pk}

    # def on_success(self, retval, task_id, args, kwargs):
    #     from .models import IngestionData, IngestionDataTask
    #     pk = retval['ingestion_request_id']
    #     i = IngestionData.objects.get(pk=pk)
    #     IngestionDataTask.objects.create(ingestion=i,
    #                                      status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.VALIDATE_COLUMN_DATA)
    #
    #
    # def on_failure(self, exc, task_id, args, kwargs, einfo):
    #     pass


class TransformationDataTask(Task):
    name = 'transformation_data_task'

    def run(self, *args, **kwargs):
        from .models import IngestionInventory
        ret = args[0]
        inventory = ret['inventory_pk']
        inv_obj = IngestionInventory.objects.get(pk=inventory)
        inv_obj.transform_data()
        return {'inventory_pk': inv_obj.pk}

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


class PreparePayloadTask(Task):
    name = 'prepare_payload_task'

    def run(self, *args, **kwargs):
        import datetime
        file_name = 'Winter Garden Theatre - NY_xyz_test_import_091019#I42PM'
        from .models import IngestionInventory
        ret = args[0]
        inventory_pk = ret['inventory_pk']
        inv_obj = IngestionInventory.objects.get(pk=inventory_pk)
        inventory_import_obj = {}
        inventory_import_obj["bulkImport_BatchID"] = 0
        inventory_import_obj["importCompanyId"] = 1
        inventory_import_obj["type"] = 1
        inventory_import_obj["deliveryType"] = 1
        inventory_import_obj["isInHand"] = True
        inventory_import_obj["isConsign"] = True
        inventory_import_obj["consignmentTerms"] = 100
        inventory_import_obj["seasonProductionIds"] = []
        inventory_import_obj["isSeason"] = False
        inventory_import_obj["fileName"] = file_name
        inventory_import_obj["importType"] = 1
        inventory_import_obj["listings"] = [
            {
                "listPriceEach": 5000.00,
                "section": "top", #str(data['section_name']),
                "row": '5', #str(data['row_name']),
                "startSeat": 22, # int(data['seat_num']),
                "endSeat": 29, #int(data['last_seat']),
                "quantity":7, #int(data['num_seats']),
                "costEach": 0.0,
                "internalNote": None,
                "externalNote": None,
                "productionId": 434399,
                "eventDate": None,
                "eventTime": None,
                "eventCity": None,
                "barcodes": []
            },
        ]
        inv_obj.payload = json.dumps(inventory_import_obj, cls=DjangoJSONEncoder)
        inv_obj.save()
        return ret



class SendInventoryTask(Task):
    name = 'send_inventory_task'

    def __init__(self):
        self.inventoryPostResponse = None

    def getToken(self):
        import requests

        url = 'https://monarchapi.azurewebsites.net/account/generatetoken'
        cred = {
            "email": "alever@dynastyse.com",
            "password": "Crescent200$",
            "rememberMe": True
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        token = requests.post(url, json=cred, headers=headers)
        return token.json()['token']

    def postInventory(self, inventory_payload):
        import requests
        inventory_import_endpoint = 'https://monarchapi.azurewebsites.net/api/inventory'
        token = self.getToken()
        headers = {
            "Authorization": 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGV2ZXJAZHluYXN0eXNlLmNvbSIsImp0aSI6IjgyMTZkMDVlLTBlMjMtNDVmNy04NmQ5LWVjY2U2M2IyZjMzNCIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvcm9sZSI6WyJtYXNzcHJpY2luZyIsIlpvbmVBc3NpZ25lciIsIlZvaWRQTyIsInZpZXdwbyIsInNhbGVzcSIsInByaWNpbmdtYW5hZ2VyIiwiaW52ZW50b3J5VjIiLCJyZXBvcnRzIiwiVXNlciIsInByb2R1Y3Rpb25tYXBwaW5nIiwiQWRtaW4iLCJmaW5SZXBvcnRzIiwicHJpY2luZyIsInZpZXdzYWxlcyIsIm1vYmlsZWZ1bGZpbGxtZW50Iiwic2VhdG1hbmFnZXIiLCJNb25hcmNoTGVnYWN5IiwiaW52ZW50b3J5IiwiQVBJIiwiU3VwZXJBZG1pbiIsImRyb3ByZXBsYWNlIiwiWm9uZXNNYW5hZ2VyIiwib3BlcmF0aW9ucyIsIlRvcGF6Il0sImV4cCI6MTU2OTE0NzQ2NiwiaXNzIjoiaHR0cDovL2FwaS5keW5hc3R5c2UuY29tIiwiYXVkIjoiaHR0cDovL2FwaS5keW5hc3R5c2UuY29tIn0.ujlM2pToKab7foG2yILIURtstou1GFRyETf6sm87fGA',
            # "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(inventory_import_endpoint, json=json.loads(inventory_payload), headers=headers)
        print('HTTP Response Status: {}'.format(response.status_code))
        return response

    def run(self, *args, **kwargs):
        res = None
        from .models import IngestionInventory
        ret = args[0]
        inventory_pk = ret['inventory_pk']
        inv_obj = IngestionInventory.objects.get(pk=inventory_pk)
        try:
            res = self.postInventory(inv_obj.payload)
            inv_obj.response = res.json()
            inv_obj.status_code = res.status_code
            inv_obj.save()
            return ret
        except Exception as e:
            if res:
                inv_obj.status_code = res.status_code
                inv_obj.save()
            raise "Unkown Error"

    def on_success(self, retval, task_id, args, kwargs):
        pass

class HandleResponseTask(Task):
    name = 'handle_response_task'

    def run(self, *args, **kwargs):
        from .models import IngestionInventory
        ret = args[0]
        inventory_pk = ret['inventory_pk']
        inv_obj = IngestionInventory.objects.get(pk=inventory_pk)
        inv_obj.handle_response()
        return {'inventory_pk': inv_obj.pk}



app.tasks.register(SelectParserTask())
app.tasks.register(InventoryIngestionTask())
app.tasks.register(ValidateFileFormatTask())
app.tasks.register(ValidateColumnNameTask())
app.tasks.register(ValidateColumnDataTask())
app.tasks.register(TransformationDataTask())
app.tasks.register(PreparePayloadTask())
app.tasks.register(SendInventoryTask())
app.tasks.register(HandleResponseTask())