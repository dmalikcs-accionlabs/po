from django.db import models
from django.contrib.contenttypes.models import ContentType

from .choices import ActionChoice, \
    ACTION_LIST
from django.conf import settings

class Rule(models.Model):
    # todoL link to parser
    name = models.CharField(max_length=75)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, null=True)


    def __str__(self):
        return str(self.pk)


class TimeBasedRule(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    action = models.CharField(max_length=10, choices=ACTION_LIST)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, null=True)


    def __str__(self):
        return str(self.id)


class FileBasedRule(models.Model):
    supported_format = models.CharField(max_length=10, choices=ACTION_LIST)
    action = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, null=True)


    def __str__(self):
        return str(self.id)