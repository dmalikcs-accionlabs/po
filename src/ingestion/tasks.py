from emerald.celery import app
from celery import  Task
from .choices import StatusChoice, \
    TaskChoice

import tablib
import magic
import time

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
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.VALIDATE_FILE_FORMAT)

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
        i = IngestionData.objects.get(pk=ret['ingestion_request_id'])
        i.status = StatusChoice.COMPLETED_FAILED
        i.save()



class ValidateColumnDataTask(Task):
    name = 'validate_column_data_task'

    def run(self, *args, **kwargs):
        print("called Validated column data")
        time.sleep(2)
        ret = args[0]
        return ret

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.VALIDATE_COLUMN_DATA)


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


class TransformationDataTask(Task):
    name = 'transformation_data_task'

    def run(self, *args, **kwargs):
        # from .models import IngestionDataAttachment
        print("called transformation data")
        time.sleep(2)
        ret = args[0]
        # attached_file = IngestionDataAttachment.objects.get(pk=ret['file_id'])
        # data = tablib.Dataset()
        # data.xls = attached_file.data_file.read()
        # print(data)
        return ret

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.TRANSFORMATION_DATA)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


class PreparePayloadTask(Task):
    name = 'prepare_payload_task'

    def run(self, *args, **kwargs):
        print("called prepare payload data")
        time.sleep(2)
        ret = args[0]
        return ret

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.PREPARE_PAYLOAD_TASK)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


class SendInventoryTask(Task):
    name = 'send_inventory_task'

    def run(self, *args, **kwargs):
        print("called send Inventory data")
        time.sleep(2)
        ret = args[0]
        return ret

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.SEND_PAYLOAD_TASK)


class HandleResponseTask(Task):
    name = 'handle_response_task'

    def run(self, *args, **kwargs):
        print("Called handleResponse Task")
        time.sleep(2)
        ret = args[0]
        return ret

    def on_success(self, retval, task_id, args, kwargs):
        from .models import IngestionData, IngestionDataTask
        pk = retval['ingestion_request_id']
        i = IngestionData.objects.get(pk=pk)
        i.status = StatusChoice.COMPLETED_SUCCESS
        i.save()
        IngestionDataTask.objects.create(ingestion=i,
                                         status=StatusChoice.COMPLETED_SUCCESS, task=TaskChoice.HANDLE_RESPONSE_TASK)

app.tasks.register(ValidateFileFormatTask())
app.tasks.register(ValidateColumnNameTask())
app.tasks.register(ValidateColumnDataTask())
app.tasks.register(TransformationDataTask())
app.tasks.register(PreparePayloadTask())
app.tasks.register(SendInventoryTask())
app.tasks.register(HandleResponseTask())

