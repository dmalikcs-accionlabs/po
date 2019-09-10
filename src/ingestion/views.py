from django.views.generic import ListView, TemplateView, \
    FormView, DetailView, RedirectView, DeleteView
from django.views.generic.edit import SingleObjectMixin
from .models import IngestionData, IngestionDataAttachment
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import get_ingestion_form
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from ingestion.models import IngestionInventory

from ingestion.serializers import IngestionInventorySerializer

from django.shortcuts import get_object_or_404

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
        parser = form.cleaned_data['parser']
        user = self.request.user
        subject = 'web upload'
        o = IngestionData.objects.create(content_type=content_type, object_id=user.pk, subject=subject, parser=parser)
        IngestionDataAttachment.objects.create(ingestion=o, data_file=file, is_supported=True)
        self.object = o
        return super(UploadInventory, self).form_valid(form)

    def get_success_url(self):
        return reverse('ingestion:ingestion_detail', args=[self.object.pk, ])

class InventoryListAPIView(generics.ListAPIView):
    serializer_class = IngestionInventorySerializer

    def get_queryset(self):
        return self.obj.ingestion_inventories.all().order_by('-created_at')

    def list(self, request, pk, *args,  **kwargs):
        self.obj = get_object_or_404(IngestionData, pk=pk)
        return super(InventoryListAPIView, self).list(request, *args, **kwargs)
#
class InventoryAPIUpdateView(APIView):
    permission_classes = []
    authentication_classes = []


    def post(self, request, *args, **kwargs):
        response_data = []
        response = {
            'data': response_data
        }
        pk = kwargs.get('pk')
        o = get_object_or_404(IngestionInventory, pk=pk)
        data = request.data['data']
        v = data[str(pk)]
        for key, value in v.items():
            o.inventory.update({key: value})
            o.save()
        inventory = o.inventory
        inventory.update({'row_Id': o.pk})
        response_data.append(inventory)
        return Response(response)


class InventoryProcessView(SingleObjectMixin, RedirectView):

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=IngestionInventory.objects.filter(deleted_at__isnull=True))
        self.object.process()
        return super(InventoryProcessView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('ingestion:ingestion_detail', args=[self.object.ingestion.pk])


class IngestionDataDeleteView(DeleteView):
    model = IngestionData
    success_url = reverse_lazy('ingestion:ingestion_list')

    def get_context_data(self, **kwargs):
        context = super(IngestionDataDeleteView, self).get_context_data(**kwargs)
        context['page_header'] = 'Ingestion'
        context['cancel_url'] = reverse('ingestion:ingestion_list')
        return context

