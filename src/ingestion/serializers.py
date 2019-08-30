from ingestion.models import IngestionInventory
from rest_framework import  serializers


class IngestionInventorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IngestionInventory
        fields = [ 'id',  'status',  ]