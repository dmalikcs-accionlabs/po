from django.views.generic import TemplateView, FormView, \
    RedirectView
from .forms import UploadForm
from django.urls import reverse, reverse_lazy
from clients.models import ClientAgent
from ingestion.models import IngestionData, \
    IngestionDataAttachment
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('dashboard:dashboard_view')


class IngestionReplicationView(FormView):
    template_name = './authentication/upload.html'
    form_class = UploadForm

    def get_success_url(self):
        return reverse('upload')

    def form_valid(self, form):
        body = form.cleaned_data['body']
        email = form.cleaned_data['email']
        subject = form.cleaned_data['subject']
        file = form.cleaned_data['file']
        object, created = ClientAgent.objects.get_or_create(email=email)
        if created:
            print("Send Information as new agent added")
        o = IngestionData.objects.create(agent=object, body=body, subject=subject)
        print("Ingestion data object created {}".format(o.subject))
        IngestionDataAttachment.objects.create(ingestion=o, data_file=file, is_supported=True)
        return super(IngestionReplicationView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IngestionReplicationView, self).get_context_data(**kwargs)
        context['enctype'] = True
        return context