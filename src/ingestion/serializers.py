from ingestion.models import IngestionInventory, \
    IngestionData
from rest_framework import  serializers

from django.utils.html import format_html
from django.urls import reverse

class IngestionInventorySerializer(serializers.ModelSerializer):
    highlight = serializers.SerializerMethodField()

    class Meta:
        model = IngestionInventory
        fields = [ 'id',  'status',  ]

    def to_representation(self, instance):
        inventory = instance.inventory
        inventory.update({
            'row_Id': instance.pk,
            'action': self.get_highlight(instance),
            'status': self.get_status(instance)
        })
        return inventory

    def get_highlight(self, obj):
        actions = IngestionData.get_action_button(obj)
        return actions

    def get_status(self, obj):
        return obj.get_status()