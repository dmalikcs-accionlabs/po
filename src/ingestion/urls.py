__author__ = 'dmalik'
from django.urls import path

from ingestion.views import IngestionDataList, \
    IngestionDataView, UploadInventory, InventoryProcessView


urlpatterns = [

    path('ingestions/', IngestionDataList.as_view(
    ), name="ingestion_list"),

    path('ingestions/<int:pk>/', IngestionDataView.as_view(
    ), name="ingestion_detail"),

    path('inventory/<int:pk>/', InventoryProcessView.as_view(
    ), name="inventory_process"),

    path('upload/inventory/', UploadInventory.as_view(
    ), name="upload_inventory"),

]

