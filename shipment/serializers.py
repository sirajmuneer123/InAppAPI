from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.serializers import SerializerMethodField, CharField




from shipment.models import (
    ShipmentType, Shipment, Products, ShipmentDetails,
    StatusCatlog, ShipmentStatus, 
)

class ShipmentDetailSerializer(ModelSerializer):
    class Meta:
        model = ShipmentDetails
        fields = '__all__'
        depth = 2



class ProductsSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class ShipmentTypeSerializer(ModelSerializer):
    class Meta:
        model = ShipmentType
        fields = '__all__'

