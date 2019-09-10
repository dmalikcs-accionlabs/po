__author__ = 'dmalik'
from django.urls import path

from parser_conf.views import ParserListView, \
    ParserUpdateWithInlineView, ParserCreateWithInlineView, \
    CollectionListView, ParseDeleteView, MessageNotificationFormset, \
    EmailNotificationFormset, ReportFormset

urlpatterns = [

    path('', ParserListView.as_view(
    ), name="parser_list"),
    path('<int:pk>/edit/', ParserUpdateWithInlineView.as_view(
    ), name="parser_edit"),

     path('<int:pk>/message/', MessageNotificationFormset.as_view(
    ), name="post_parser_message"),

    path('<int:pk>/email/', EmailNotificationFormset.as_view(
    ), name="post_parser_email"),

    path('<int:pk>/reports/', ReportFormset.as_view(
    ), name="post_parser_report"),


    path('<int:pk>/delete/', ParseDeleteView.as_view(
    ), name="parser_delete"),
    path('add/<int:collection_id>/', ParserCreateWithInlineView.as_view(
    ), name="parser_add"),
    path('collections/', CollectionListView.as_view(
    ), name="collection_list"),

]

