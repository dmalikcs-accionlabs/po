from django.db import models
from .choices import STATUS_CHOICE_STATUS, \
    StatusChoice, TaskChoice, TASK_CHOICE_LIST
from .tasks import ValidateFileFormatTask, ValidateColumnNameTask, \
    ValidateColumnDataTask, TransformationDataTask, PreparePayloadTask, \
    SendInventoryTask, HandleResponseTask
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import HStoreField, JSONField, \
    ArrayField
import tablib
import json
from django.contrib.contenttypes.fields import GenericRelation


class IngestionData(models.Model):
    agent = models.ForeignKey('clients.ClientAgent', on_delete=models.PROTECT, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True,)
    subject = models.CharField(max_length=256, blank=True)
    body = models.TextField(null=True, blank=True)
    can_process = models.BooleanField(default=False)
    status = models.CharField(max_length=5, choices=STATUS_CHOICE_STATUS, default=StatusChoice.NEW)
    notes = models.TextField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, editable=False, on_delete=models.SET_NULL)
    txt_notifications = GenericRelation('notification.TextNotification')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        created = self._state.adding
        # if self.content_object.client and self.content_object.client.get_parsers():
        #     self.can_process = True
        # else:
        self.status = StatusChoice.STOPED
        super(IngestionData, self).save(*args, **kwargs)

        if created and not self.can_process:
            notes = 'Client or Parser is not defined for incoming email.'
            IngestionDataTask.objects.create(ingestion=self, status=StatusChoice.STOPED, task=TaskChoice.ACK_STOPED, notes=notes)
        if created and self.can_process:
            pk = self.pk
            validated_fileformat_task = ValidateFileFormatTask()
            validate_columnname_task = ValidateColumnNameTask()
            validate_columndata_task = ValidateColumnDataTask()
            transformation_data_task = TransformationDataTask()
            prepare_payload_task = PreparePayloadTask()
            send_inventory_task = SendInventoryTask()
            handle_response_task = HandleResponseTask()
            chain = validated_fileformat_task.s(pk) | validate_columnname_task.s() | validate_columndata_task.s() | \
                    transformation_data_task.s() | prepare_payload_task.s() | send_inventory_task.s() | handle_response_task.s()
            chain()

    def get_agent(self):
        return self.agent

    def get_attached_files(self):
        return self.ingestion_files.all()

    def get_attached_files_count(self):
        return self.ingestion_files.count()

    def get_parsers(self):
        return self.agent.get_parsers()

    def get_task_count(self):
        return self.ingestion_tasks.count()

    def get_inventory_count(self):
        return self.ingestion_inventories.count()

    def get_headers(self):
        files  = self.get_attached_files()
        if len(files) >= 1: f = files[0]
        return f.headers

    def get_inventory(self):
        headers = self.get_headers()
        rows = []
        print(headers)
        for i in self.ingestion_inventories.all():
            pass
            rows.append([ i.inventory.get(header, None) for header in headers ])

        return rows



class IngestionDataTask(models.Model):
    ingestion = models.ForeignKey('ingestion.IngestionData', on_delete=models.CASCADE, related_name='ingestion_tasks')
    status = models.CharField(max_length=35, choices=STATUS_CHOICE_STATUS)
    task = models.CharField(max_length=35, choices=TASK_CHOICE_LIST)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return "{}".format(self.pk)


class IngestionDataAttachment(models.Model):
    ingestion = models.ForeignKey('ingestion.IngestionData', on_delete=models.CASCADE, related_name='ingestion_files')
    headers = ArrayField(models.CharField(max_length=128), null=True)
    name = models.CharField(max_length=125, blank=True, editable=False)
    f_format = models.CharField(max_length=10, null=True, editable=False)
    is_supported = models.BooleanField(editable=False)
    data_file = models.FileField(upload_to='./ingestion_data/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        created = self._state.adding
        super(IngestionDataAttachment, self).save(*args, **kwargs)
        if created:
            self.load_inventory()

    def load_inventory(self):
        if self.data_file and self.is_supported:
            dataset = tablib.Dataset()
            dataset.xls = self.data_file.read()
            self.headers = dataset.headers
            self.save()
            for inventory in json.loads(dataset.export('json')):
                IngestionInventory.objects.create(ingestion=self.ingestion, inventory=inventory)


class IngestionInventory(models.Model):
    ingestion = models.ForeignKey('ingestion.IngestionData', on_delete=models.CASCADE, related_name='ingestion_inventories')
    status = models.CharField(max_length=2, default='N')
    inventory = HStoreField()
    batch_id = models.CharField(max_length=35, null=True)
    payload = JSONField(null=True)
    response = JSONField(null=True)
    processed_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return str(self.id)