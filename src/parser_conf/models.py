from django.db import models
from .choices import SupportedFileFormatChoice, SUPPORTED_FILE_FORMAT_LIST, \
    COLUMN_CHOICE_LIST, ColumnChoice, ShareChoice, SHARE_CHOICE_LIST, DATEFormatChoice, \
    DATE_FORMAT_CHOICE_LIST, DATA_TYPE_CHOICES
from django.conf import settings
from django.contrib.postgres.fields import HStoreField
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from utils.models import MobileValidation
from django.contrib.contenttypes.fields import GenericForeignKey
from collections import namedtuple

class ParserCollection(models.Model):
    name = models.CharField(max_length=75)
    brief = models.TextField(blank=True)
    endpoint = models.URLField(blank=True, editable=False)
    # columns = HStoreField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleated_at = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return self.name


class ParserCollectionColumm(models.Model):
    collection = models.ForeignKey(ParserCollection, on_delete=models.CASCADE, related_name='columns')
    column_name = models.CharField('expected column', max_length=75)
    payload = models.CharField('map column', max_length=75)
    data_type = models.CharField(max_length=10, null=True,
                                 choices=DATA_TYPE_CHOICES)
    is_required = models.BooleanField('required', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}-{}".format(self.column_name, self.column_name)


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

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()

    def get_expected_columns(self):
        return [conf.column_name for conf in self.config_maps.all()]

    def get_mapped_columns(self):
        return [conf.payload for conf in self.config_maps.all()]

    def get_transform_payload(self):
        return [(conf.column_name, conf.payload) for conf in self.config_maps.all()]

    def get_columns_with_datatype(self):
        Column = namedtuple('Column', ['column_name', 'payload', 'datatype'])
        return [
            Column(conf.column_name, conf.payload, self.collection.columns.get(payload=conf.payload).datatype)
            for conf in self.config_maps.all()
        ]



class ColumnPayloadMap(models.Model):
    config = models.ForeignKey(ParserConfigurationDef, on_delete=models.CASCADE, related_name='config_maps')
    column_name = models.CharField('expected column', max_length=75)
    payload = models.CharField('map column', max_length=75)
    is_required = models.BooleanField('required', default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        unique_together = ('config', 'payload')

    def __str__(self):
        return '{}-{}'.format(self.column_name, self.payload)


class PostIngestion(models.Model):
    parser = models.ForeignKey(ParserConfigurationDef, on_delete=models.CASCADE, related_name='post_ingestions')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return str(self.parser)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.save()


class EmailNotification(models.Model):
    parser = models.ForeignKey(ParserConfigurationDef, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        created = self._state.adding
        super(EmailNotification, self).save(*args, **kwargs)
        if created:
            i = PostIngestion.objects.create(parser=self.parser, content_object=self)


class TextNotification(models.Model):
    parser = models.ForeignKey(ParserConfigurationDef, on_delete=models.CASCADE, null=True)
    mobile = models.CharField(max_length=10, validators=[MobileValidation, ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        created = self._state.adding
        super(TextNotification, self).save(*args, **kwargs)
        if created:
            i = PostIngestion.objects.create(parser=self.parser, content_object=self)


class PostIngestionReport(models.Model):
    REPORT = (
        ('SUM', 'Summary'),
    )
    parser = models.ForeignKey(ParserConfigurationDef, on_delete=models.CASCADE, null=True)
    report = models.CharField(max_length=10, choices=REPORT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.report

    def save(self, *args, **kwargs):
        created = self._state.adding
        super(PostIngestionReport, self).save(*args, **kwargs)
        if created:
            i = PostIngestion.objects.create(parser=self.parser, content_object=self)
