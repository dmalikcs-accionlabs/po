__author__ = 'dmalik'
from django.urls import path

from ingestion.views import IngestionDataList, \
    IngestionDataView, UploadInventory, InventoryProcessView, \
    IngestionDataDeleteView


urlpatterns = [

    path('ingestions/', IngestionDataList.as_view(
    ), name="ingestion_list"),

    path('ingestions/<int:pk>/', IngestionDataView.as_view(
    ), name="ingestion_detail"),

    path('ingestions/<int:pk>/delete/', IngestionDataDeleteView.as_view(
    ), name="ingestion_delete"),

    path('inventory/<int:pk>/', InventoryProcessView.as_view(
    ), name="inventory_process"),

    path('upload/inventory/', UploadInventory.as_view(
    ), name="upload_inventory"),

]

