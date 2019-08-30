__author__ = 'dmalik'
from django.urls import path

from parser_conf.views import ParserListView, \
    ParserUpdateWithInlineView, ParserCreateWithInlineView, \
    CollectionListView

urlpatterns = [

    path('', ParserListView.as_view(
    ), name="parser_list"),
    path('<int:pk>/edit/', ParserUpdateWithInlineView.as_view(
    ), name="parser_edit"),
    path('add/<int:collection_id>/', ParserCreateWithInlineView.as_view(
    ), name="parser_add"),
    path('collections/', CollectionListView.as_view(
    ), name="collection_list"),

]

