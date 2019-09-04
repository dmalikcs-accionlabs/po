from rest_framework import serializers, status
from clients.models import ClientAgent
from ingestion.models import IngestionData, \
    IngestionDataAttachment
from rest_framework.response import Response

class IngestionSerializer(serializers.Serializer):

    email = serializers.EmailField()
    body = serializers.CharField(allow_blank=True)
    subject = serializers.CharField(max_length=200, allow_blank=True)
    attachment    = serializers.FileField(allow_empty_file=False, use_url='./ingestion_data/')
    ingestion_id = serializers.IntegerField(read_only=True, allow_null=True)


    def create(self, validated_data):
        body = validated_data.get('body')
        email = validated_data.get('email')
        subject = validated_data.get('subject')
        file = validated_data.get('file')
        object, created = ClientAgent.objects.get_or_create(email=email)
        if created:
            print("Send Information as new agent added")
        o = IngestionData.objects.create(agent=object, body=body, subject=subject)
        print("Ingestion data object created {}".format(o.subject))
        i = IngestionDataAttachment.objects.create(ingestion=o, data_file=file, is_supported=True)
        return {'body': o.body, 'email': object.email,  'subject':o.subject, 'attachment': i.pk, 'ingestion_id': o.pk}