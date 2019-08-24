from django.db import models
from clients.models import ClientAgent

class IngestionData(models.Model):
    agent = models.ForeignKey(ClientAgent, on_delete=models.PROTECT)
    subject = models.CharField(max_length=256)
    body = models.TextField(null=True)
    is_proceed = models.BooleanField(default=True)
    created_t  = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.agent

    def get_attached_files(self):
        return self.ingestion_set.all()


class IngestionDataAttachment(models.Model):
    ingestion = models.ForeignKey(IngestionData, on_delete=models.CASCADE)
    name = models.CharField(max_length=125)
    f_format = models.CharField(max_length=10, null=True, editable=False)
    is_supported = models.BooleanField(editable=False)
    data_file = models.FileField(upload_to='./ingestion_data/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(editable=False, null=True)

    def __str__(self):
        return self.name
