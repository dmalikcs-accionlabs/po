from django.db import models

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation


class TextNotification(models.Model):

    reference_content_type = models.ForeignKey(ContentType, related_name='reference', null=True, editable=True, on_delete=models.SET_NULL)
    reference_object_id = models.CharField(max_length=36, null=True, editable=True)
    reference_content_object = GenericForeignKey('reference_content_type', 'reference_object_id')

    content_type = models.ForeignKey(ContentType,
                                     # limit_choices_to={
        # 'app_label__in': [Student._meta.app_label, Employee._meta.app_label,],
        # 'model__in': [Student._meta.model_name, Employee._meta.model_name, ],
    # },
                                     on_delete=models.CASCADE)
    object_id = models.CharField(max_length=36 )
    content_object = GenericForeignKey('content_type', 'object_id')


    cnt_code = models.IntegerField(default='001', editable=False, null=False)
    contact_number = models.IntegerField()
    msg = models.TextField()
    is_dispatched = models.BooleanField()
    is_delivered = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.contact_number

    def save(self, *args, **kwargs):
        created = self._state.adding
        super(TextNotification, self).save(*args, **kwargs)
        if created:
            self.send_txt()

    def send_txt(self):
        print("sending message from txt ")