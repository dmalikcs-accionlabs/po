from ingestion.models import IngestionInventory
from rest_framework import  serializers


class IngestionInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IngestionInventory
        fields = [ 'id',  'status', '' ]

    def to_representation(self, instance):
        inventory = instance.inventory
        inventory.update({'row_Id': instance.pk})
        return inventory