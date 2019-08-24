from django.db import models

from parser_conf.models import ParserConfigurationDef


class Client(models.Model):
    name = models.CharField(max_length=75)
    parser = models.ManyToManyField(ParserConfigurationDef)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name


class ClientAgent(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=75, null=True)
    email = models.EmailField(unique=True)
    is_logged_allowed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.name if self.name else self.email

    def save(self, *args, **kwargs):
        # send create user signals as soon as logged
        super(ClientAgent, self).save(*args, **kwargs)