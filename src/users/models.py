__author__ = 'dmalik'
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.contrib.contenttypes.fields import GenericRelation
from ingestion.models import IngestionData
from clients.models import Client
class CustomUserManager(UserManager):
    pass

class User(AbstractUser):
    client = models.ForeignKey(Client, null=True, on_delete=models.PROTECT)
    ingestions = GenericRelation(IngestionData)
