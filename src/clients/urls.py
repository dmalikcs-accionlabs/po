__author__ = 'dmalik'
from django.urls import path

from clients.views import ClientListView, \
    AgentListView, ClientDetailView, AgentDetailView, \
    ClientEditView, AgentEditForm, ClientAddView, AgentAddForm, \
    AgentDeleteView, ClientDeletelView

urlpatterns = [

    path('clients/', ClientListView.as_view(
    ), name="client_list"),
    path('client/<int:pk>/', ClientDetailView.as_view(
    ), name="client_detail"),
    path('client/<int:pk>/edit/', ClientEditView.as_view(
    ), name="client_edit"),
    path('client/<int:pk>/delete/', ClientDeletelView.as_view(
    ), name="client_delete"),
    path('client/add/', ClientAddView.as_view(
    ), name="client_add"),

    path('agents/', AgentListView.as_view(
    ), name="agent_list"),
    path('agents/<int:pk>/', AgentDetailView.as_view(
    ), name="agent_detail"),
    path('agents/<int:pk>/edit/', AgentEditForm.as_view(
    ), name="agent_edit"),
    path('agents/<int:pk>/delete/', AgentDeleteView.as_view(
    ), name="agent_delete"),
    path('agents/add/', AgentAddForm.as_view(
    ), name="agent_add"),

]

