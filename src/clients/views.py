from django.views.generic import ListView, TemplateView, DetailView, \
    UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from clients.models import Client, ClientAgent
from django.http import HttpResponseForbidden

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'clients/clients_list.html'

    def get(self, request, *args, **kwargs):
        u = request.user
        if not u.is_staff:
            return HttpResponseForbidden()
        return super(ClientListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(deleted_at__isnull=True)

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['page_header'] = 'Clients'
        return context


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        context['page_header'] = 'Clients'
        return context


class ClientEditView(LoginRequiredMixin, UpdateView):
    model = Client

    def get_form_class(self):
        from .forms import ClientForm
        return ClientForm

    def get_success_url(self):
        return reverse('clients:client_edit', args=[self.object.pk, ])

    def get_context_data(self, **kwargs):
        context = super(ClientEditView, self).get_context_data(**kwargs)
        context['page_header'] = 'Clients'
        return context


class ClientAddView(LoginRequiredMixin, CreateView):
    model = Client

    def get(self, request, *args, **kwargs):
        u = request.user
        if not u.is_staff:
            return HttpResponseForbidden()
        return super(ClientAddView, self).get(request, *args, **kwargs)

    def get_form_class(self):
        from .forms import ClientForm
        return ClientForm

    def get_success_url(self):
        return reverse('clients:client_edit', args=[self.object.pk, ])

    def get_context_data(self, **kwargs):
        context = super(ClientAddView, self).get_context_data(**kwargs)
        context['page_header'] = 'Clients'
        return context


class AgentListView(LoginRequiredMixin, ListView):
    model = ClientAgent
    template_name =  'clients/agent_list.html'

    def get(self, request, *args, **kwargs):
        u = request.user
        if not u.is_staff:
            return HttpResponseForbidden()
        return super(AgentListView, self).get(request,  *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AgentListView, self).get_context_data(**kwargs)
        context['page_header'] = 'Agents'
        return context


class AgentDetailView(LoginRequiredMixin, DetailView):
    model = ClientAgent
    template_name =  'clients/agent_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        context['page_header'] = 'Agents'
        return context


class AgentEditForm(LoginRequiredMixin, UpdateView):
    model = ClientAgent
    template_name = 'clients/clientagent_form.html'

    def get_form_class(self):
        from .forms import ClientAgentForm
        return ClientAgentForm

    def get_success_url(self):
        return reverse('clients:agent_edit', args=[self.object.pk, ])

    def get_context_data(self, **kwargs):
        context = super(AgentEditForm, self).get_context_data(**kwargs)
        context['page_header'] = 'Agents'
        return context


class AgentAddForm(LoginRequiredMixin, CreateView):
    model = ClientAgent
    template_name = 'clients/clientagent_form.html'

    def get_form_class(self):
        from .forms import ClientAgentForm
        return ClientAgentForm

    def get_success_url(self):
        return reverse('clients:agent_edit', args=[self.object.pk, ])

    def get_context_data(self, **kwargs):
        context = super(AgentAddForm, self).get_context_data(**kwargs)
        context['page_header'] = 'Agents'
        return context