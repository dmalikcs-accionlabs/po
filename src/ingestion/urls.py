__author__ = 'dmalik'
from django.urls import path

from ingestion.views import IngestionDataList, \
    IngestionDataView, UploadInventory


urlpatterns = [

    path('ingestions/', IngestionDataList.as_view(
    ), name="ingestion_list"),

    path('ingestions/<int:pk>/', IngestionDataView.as_view(
    ), name="ingestion_detail"),

    path('upload/inventory/', UploadInventory.as_view(
    ), name="upload_inventory"),

]

