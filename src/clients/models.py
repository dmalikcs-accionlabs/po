from django.db import models

from parser_conf.models import ParserConfigurationDef
from ingestion.models import IngestionData
from ingestion.choices import StatusChoice as IngestionStatusChoice


class Client(models.Model):
    name = models.CharField(max_length=75)
    external_clientid = models.CharField(max_length=10, null=True)
    parser = models.ManyToManyField(ParserConfigurationDef)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.name

    def get_agents_count(self):
        return self.agents.filter(deleted_at__isnull=True).count()

    def get_agents(self):
        return self.agents.filter(deleted_at__isnull=True)

    def get_parser_count(self):
        return self.parser.filter(deleted_at__isnull=True).count()

    def get_parsers(self):
        return self.parser.filter(deleted_at__isnull=True)

    def get_ingestions(self):
        agents = self.agents.filter(deleted_at__isnull=True)
        return IngestionData.objects.filter(agent__in=agents).order_by('-created_at')

    def get_ingestions_count(self):
        agents = self.agents.filter(deleted_at__isnull=True)
        return IngestionData.objects.filter(agent__in=agents).count()

    def get_ingestions_completed_count(self):
        agents = self.agents.filter(deleted_at__isnull=True)
        return IngestionData.objects.filter(agent__in=agents, status=IngestionStatusChoice.COMPLETED_SUCCESS).count()

    def get_ingestions_failed_count(self):
        agents = self.agents.filter(deleted_at__isnull=True)
        return IngestionData.objects.filter(agent__in=agents, status=IngestionStatusChoice.COMPLETED_FAILED).count()

    def get_ingestions_running_count(self):
        agents = self.agents.filter(deleted_at__isnull=True)
        return IngestionData.objects.filter(agent__in=agents, status__in=[IngestionStatusChoice.NEW, ]).count()



class ClientAgent(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, related_name='agents')
    name = models.CharField(max_length=75, null=True)
    email = models.EmailField(unique=True)
    is_logged_allowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, editable=False)

    def __str__(self):
        return self.name if self.name else self.email

    def save(self, *args, **kwargs):
        # send create user signals as soon as logged
        super(ClientAgent, self).save(*args, **kwargs)

    def get_client(self):
        return self.client.name if self.client else ''

    def get_parsers(self):
        return self.client.get_parsers() if self.client else None

    def get_parser_count(self):
        return self.client.get_parser_count() if self.client else None

    def get_ingestions(self):
        return IngestionData.objects.filter(agent=self).order_by('-created_at')

    def get_ingestions_count(self):
        return IngestionData.objects.filter(agent=self).count()

    def get_ingestions_completed_count(self):
        return IngestionData.objects.filter(agent=self, status=IngestionStatusChoice.COMPLETED_SUCCESS).count()

    def get_ingestions_failed_count(self):
        return IngestionData.objects.filter(agent=self, status=IngestionStatusChoice.COMPLETED_FAILED).count()

    def get_ingestions_running_count(self):
        return IngestionData.objects.filter(agent=self, status__in=[IngestionStatusChoice.NEW, ]).count()

