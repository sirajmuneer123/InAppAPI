from django.contrib import admin
from django.urls import path
from shipment.views import (
    ShipmentData, ShipmentListAPIView, Predata
)


urlpatterns = [
    path('shipment/<pk>/', ShipmentData.as_view(), name='shipment-detail'),
    path('shipment/', ShipmentData.as_view(), name='shipment'),
    path('shipment-list/', ShipmentListAPIView.as_view(), name='shipment-list'),
    path('predata/', Predata.as_view(), name='predata'),
]
