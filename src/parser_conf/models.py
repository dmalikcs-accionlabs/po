from django.db import models
from .choices import SupportedFileFormatChoice, SUPPORTED_FILE_FORMAT_LIST, \
    COLUMN_CHOICE_LIST, ColumnChoice, ShareChoice, SHARE_CHOICE_LIST, DATEFormatChoice, \
    DATE_FORMAT_CHOICE_LIST
from django.conf import settings
from django.contrib.postgres.fields import HStoreField


class ParserCollection(models.Model):
    name = models.CharField(max_length=75)
    brief = models.TextField(blank=True)
    endpoint = models.URLField(blank=True, editable=False)
    columns = HStoreField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleated_at = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return self.name


class ParserConfigurationDef(models.Model):
    collection = models.ForeignKey(ParserCollection, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=75)
    brief = models.TextField(null=True, blank=True)

    date_format = models.CharField(max_length=35, choices=DATE_FORMAT_CHOICE_LIST,
                                   default=DATEFormatChoice.DDMMYYYY, editable=False)


    f_format = models.CharField('supported file', max_length=35, choices=SUPPORTED_FILE_FORMAT_LIST,
                                default=SupportedFileFormatChoice.XLS, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False, null=True, on_delete=models.SET_NULL)
    share_option = models.CharField(max_length=15, choices=SHARE_CHOICE_LIST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        verbose_name = 'global parser configuration'
        verbose_name_plural = 'global parser configurations'

    def __str__(self):
        return self.name

    def get_expected_columns(self):
        return [conf.column_name for conf in self.config_maps.all()]

    def get_mapped_columns(self):
        return [conf.payload for conf in self.config_maps.all()]

    def get_transform_payload(self):
        return [(conf.column_name, conf.payload )for conf in self.config_maps.all()]

class ColumnPayloadMap(models.Model):
    config = models.ForeignKey(ParserConfigurationDef, on_delete=models.CASCADE, related_name='config_maps')
    column_name = models.CharField('expected column', max_length=75)
    payload = models.CharField('map column', max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        unique_together = ('config', 'payload')

    def __str__(self):
        return '{}-{}'.format(self.column_name, self.payload)

