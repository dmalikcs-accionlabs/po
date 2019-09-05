from django.db import models
from .choices import STATUS_CHOICE_STATUS, \
    StatusChoice, TaskChoice, TASK_CHOICE_LIST, \
    INVENTORYSTATUSCHOICE_LIST, InventoryStatusChoice
from .tasks import ValidateFileFormatTask, ValidateColumnNameTask, \
    ValidateColumnDataTask, TransformationDataTask, PreparePayloadTask, \
    SendInventoryTask, HandleResponseTask, SelectParserTask, InventoryIngestionTask
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import HStoreField, JSONField, \
    ArrayField
import tablib
import json
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.html import format_html, mark_safe
from django.utils.timezone import now
from django.urls import reverse

class IngestionData(models.Model):
    agent = models.ForeignKey('clients.ClientAgent', on_delete=models.PROTECT, null=True)
    parser = models.ForeignKey('parser_conf.ParserConfigurationDef', editable=False, null=True, on_delete=models.PROTECT)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True,)

    subject = models.CharField(max_length=256, blank=True)
    body = models.TextField(null=True, blank=True)
    can_process = models.BooleanField(default=False)

    status = models.CharField(max_length=5, choices=STATUS_CHOICE_STATUS, default=StatusChoice.NEW)
    notes = models.TextField(blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, editable=False, on_delete=models.SET_NULL)
    einfo = models.TextField(null=True, editable=False)
    txt_notifications = GenericRelation('notification.TextNotification')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        created = self._state.adding
        # if self.content_object.client and \
        #         self.content_object.client.get_parsers():
        #     self.can_process = True
        # else:
        #     self.status = StatusChoice.NEW
        super(IngestionData, self).save(*args, **kwargs)

        # if created:
        #     notes = 'Client or Parser is not defined for incoming email.'
        #     IngestionDataTask.objects.create(ingestion=self,
        #                                      status=StatusChoice.STOPED,
        #                                      task=TaskChoice.ACK_STOPED, notes=notes)
        if created and self.parser:
            self.execute_ingestion_process()

        if created and not self.parser:
            select_parser = SelectParserTask()
            select_parser.apply_async(args= [self.pk, ])

    def execute_ingestion_process(self):
        validated_fileformat_task = ValidateFileFormatTask()
        validate_columnname_task = ValidateColumnNameTask()
        invetory_ingestion_task = InventoryIngestionTask()

        chain = validated_fileformat_task.s(self.pk) | validate_columnname_task.s() | invetory_ingestion_task.s()
        chain()

    def get_agent(self):
        return self.agent

    def get_attached_files(self):
        return self.ingestion_files.all()

    def get_attached_files_count(self):
        return self.ingestion_files.count()

    def get_parsers(self):
        return [self.parser, ]

    def get_task_count(self):
        return self.ingestion_tasks.count()

    def get_inventory_count(self):
        return self.ingestion_inventories.count()

    def get_headers(self):
        files  = self.get_attached_files()
        if len(files) >= 1: f = files[0]
        return f.headers

    def get_action_button(self, row):
        if row.status == InventoryStatusChoice.NEW:
            return mark_safe("""
            <a href='{}'>
            <i class='fa fa-play'></i>
            </a>""".format(reverse('ingestion:inventory_process', args=[row.pk, ])))
        elif row.status == InventoryStatusChoice.QUEUE:
            return mark_safe("""
            <a href='{}'>
            <i class='fa fa-clock-o'></i>
            </a>""".format(reverse('ingestion:inventory_process', args=[row.pk, ])))
        else:
            return mark_safe("""
                        <a href='{}'>
                        <i class='fa fa-history'></i>
                        </a>""".format(reverse('ingestion:inventory_process', args=[row.pk, ])))

    def get_inventory(self):
        headers = self.get_headers()
        rows = []
        for i in self.ingestion_inventories.all():
            r = [ i.inventory.get(header, None) for header in headers ]
            r.append(self.get_action_button(i))
            rows.append(r)
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

    def get_parser(self):
        return self.ingestion.parser

class IngestionInventory(models.Model):
    ingestion = models.ForeignKey('ingestion.IngestionData', on_delete=models.CASCADE, related_name='ingestion_inventories')
    status = models.CharField(max_length=2, default=InventoryStatusChoice.NEW)
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

    def can_process(self):
        return True if self.ingestion.parser else False

    def process(self):
        validate_columndata_task = ValidateColumnDataTask()
        transformation_data_task = TransformationDataTask()

        prepare_payload_task = PreparePayloadTask()
        send_inventory_task = SendInventoryTask()
        handle_response_task = HandleResponseTask()

        chain = validate_columndata_task.s(self.pk) | \
          transformation_data_task.s() | prepare_payload_task.s() | send_inventory_task.s() | handle_response_task.s()
        chain()
        self.processed_at = now()
        self.status = InventoryStatusChoice.QUEUE
        self.save()

    def validate_data(self):
        pass

    def transform_data(self):
        payload_dict = {}
        parser = self.ingestion.parser
        if parser:
            for column, payload  in parser.get_transform_payload():
                payload_dict.update(
                    {
                        payload: self.inventory[column]
                    }
                )
        self.payload = payload_dict
        self.save()

    def send_data(self):
        pass

    def handle_response(self):
        self.status = InventoryStatusChoice.UPLOADED
        self.save()