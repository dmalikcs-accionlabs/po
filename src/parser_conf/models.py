from django.db import models
from .choices import SupportedFileFormatChoice, SUPPORTED_FILE_FORMAT_LIST, \
    COLUMN_CHOICE_LIST, ColumnChoice


class ParserConfigurationDef(models.Model):
    name = models.CharField(max_length=75)
    f_format = models.CharField(max_length=35, choices=SUPPORTED_FILE_FORMAT_LIST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'global parser configuration'
        verbose_name_plural = 'global parser configurations'

    def __str__(self):
        return self.name


class ColumnPayloadMap(models.Model):
    config = models.ForeignKey(ParserConfigurationDef, on_delete=models.PROTECT)
    column_name = models.CharField(max_length=75)
    payload = models.CharField(max_length=10, choices=COLUMN_CHOICE_LIST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    class Meta:
        unique_together = ('config', 'payload')

    def __str__(self):
        return '{}-{}'.format(self.column_name, self.get_payload_display())

