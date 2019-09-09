from emerald.celery import app
from celery import  Task
from .choices import StatusChoice, \
    TaskChoice

import tablib
import magic
import time


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
        IngestionDataTask.objects.\
            create(ingestion=i, task=TaskChoice.ACK, status=StatusChoice.STOPED, notes='Unable to find parser')


class ValidateFileFormatTask(Task):
    name = 'validate_file_format_task'

    def run(self, *args, **kwargs):
        from .models import IngestionData
        pk = args[0]
        i = IngestionData.objects.get(pk=pk)
        for attachment in i.get_attached_files():
            if magic.from_buffer(attachment.data_file.read(), mime=True) \
                    in ['application/vnd.ms-office', ]:
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
            applied_parser = parser
            expected_headers = self.get_expected_headers(parser=parser)
            for header in expected_headers:
                if not header.lower() in received_headers:
                    applied_parser = None
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
        from .models import IngestionData
        ret = args[0]
        i = IngestionData.objects.get(pk=ret)
        i.status = StatusChoice.COMPLETED_FAILED
        i.save()



class InventoryIngestionTask(Task):
    name = 'inventory_ingestion_task'

    def run(self, *args, **kwargs):
        from .models import IngestionData, IngestionDataTask
        time.sleep(2)
        ret = args[0]
        ingestion_obj = IngestionData.objects.get(pk=ret['ingestion_request_id'])
        for inventory in ingestion_obj.ingestion_inventories.all():
            inventory.process()
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
        from .eibo_payload import PreparePayload
        ret = args[0]
        inventory = ret['inventory_pk']
        inv_obj = PreparePayload.objects.get(pk=inventory) # what is the use of this line
        return {'inventory_pk': inv_obj.pk}

class SendInventoryTask(Task):
    name = 'send_inventory_task'

    def __init__(self):
        self.inventoryPostResponse = None

    def postInventory(self, token, inventory_payload):
        import requests
        inventory_import_endpoint = 'https://api.dynastyse.com/api/inventory'
        headers = {
            "Authorization": f'Bearer {token}'
        }
        self.inventoryPostResponse = requests.post(inventory_import_endpoint, json=inventory_payload, headers=headers)

    def run(self, *args, **kwargs):
            from .models import IngestionInventory
            ret = args[0]
            inventory = ret['inventory_pk']
            inv_obj = IngestionInventory(performer='', venue='',
                                         eventdate='', eventtime='',
                                         vendor='',
                                         fee=0).create_inventory_object(file_seatblocks='')
            return {'inventory_pk': inv_obj.pk}

    def on_success(self, retval, task_id, args, kwargs):
        pass


class HandleResponseTask(Task):
    name = 'handle_response_task'

    def run(self, *args, **kwargs):
        from .models import IngestionInventory
        ret = args[0]
        inventory = ret['inventory_pk']
        inv_obj = IngestionInventory.objects.get(pk=inventory)
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

