from django.views.generic import ListView, TemplateView, FormView, DetailView
from .models import IngestionData, IngestionDataAttachment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import get_ingestion_form
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

class IngestionDataList(LoginRequiredMixin, ListView):
    model = IngestionData
    template_name = 'ingestion/ingestion_data_list.html'

    def get_queryset(self):
        u = self.request.user
        if u.is_staff:
            return self.model.objects.filter(deleted_at__isnull=True).order_by('-created_at')
        return u.ingestions.filter(deleted_at__isnull=True).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(IngestionDataList, self).get_context_data()
        context['page_header'] = 'Ingestion'
        return context


class IngestionDataView(LoginRequiredMixin, DetailView):
    model = IngestionData
    template_name =  'ingestion/ingestion_data_detail.html'

    def get_context_data(self, **kwargs):
        context = super(IngestionDataView, self).get_context_data()
        context['page_header'] = 'Ingestion'
        context['txt_notifications'] = self.object.txt_notifications.all()
        return context

class UploadInventory(FormView):
    template_name = 'ingestion/upload_inventory.html'
    object = None

    def get_context_data(self, **kwargs):
        context = super(UploadInventory, self).get_context_data(**kwargs)
        context['page_header'] = 'Upload inventory'
        context['enctype'] = True
        return context

    def get_form_class(self):
        return get_ingestion_form(self.request.user)

    def form_valid(self, form):
        content_type = ContentType.objects.get_for_model(get_user_model())
        file = form.cleaned_data['file']
        user = self.request.user
        subject = 'web upload'
        o = IngestionData.objects.create(content_type=content_type, object_id=user.pk, subject=subject)
        IngestionDataAttachment.objects.create(ingestion=o, data_file=file, is_supported=True)
        self.object = o
        return super(UploadInventory, self).form_valid(form)

    def get_success_url(self):
        return reverse('ingestion:ingestion_detail', args=[self.object.pk, ])
#

from rest_framework.views import APIView
from rest_framework.response import Response
from ingestion.models import IngestionInventory


from ingestion.serializers import IngestionInventorySerializer

class InventoryListAPIView(APIView):

    def get(self, request, format=None):
        inventories  = IngestionInventory.objects.all()
        serializer = IngestionInventorySerializer(inventories, many=True)
        return Response(serializer.data)
