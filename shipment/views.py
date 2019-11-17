from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import ListAPIView
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
import datetime


from shipment.models import (
    ShipmentType, Shipment, Products, ShipmentDetails,
    StatusCatlog, ShipmentStatus, 
)
from shipment.serializers import (
    ShipmentDetailSerializer, 
    ShipmentTypeSerializer,
    ProductsSerializer,
)
from decimal  import Decimal

class ShipmentData(APIView):
    """ create, update, get, delete shipment
    """

    permission_classes = (AllowAny, )

    def put(self, request, pk, format=None):
        data = request.data
        obj = ShipmentDetails.objects.get(pk=pk)
        product_price = data.get('product_price')
        delivery_cost = data.get('delivery_cost')
        quantity = data.get('quantity')
        final_price = Decimal(product_price)+Decimal(delivery_cost)
        obj.shipment.shipment_type_id = data.get('shipment_type_id')
        obj.shipment.shipping_address = data.get('shipping_address')
        obj.shipment.billing_address = data.get('billing_address')
        obj.shipment.product_price = product_price
        obj.shipment.delivery_cost=delivery_cost
        obj.shipment.save()
        obj.final_price=final_price
        obj.product_id = data.get('product_id')
        obj.quantity = data.get('quantity')
        obj.price_per_unit = product_price
        obj.price = Decimal(final_price *Decimal(quantity))
        obj.save()
        return Response({'status': 'success'})
    

    def get(self, request, pk, format=None):

        try:
            shipment = ShipmentDetails.objects.get(pk=pk)
            serializer = ShipmentDetailSerializer(shipment)
            return Response({'status': 'success',
                                    'data': serializer.data})
        except ObjectDoesNotExist:
            return Response({'status': 'failed',
                            'error': 'Object does not exist'},
                            status=HTTP_400_BAD_REQUEST)
    
    def post(self, request, format=None):

        with transaction.atomic():
            data = request.data
            product_price = data.get('product_price')
            delivery_cost = data.get('delivery_cost')
            shipment = Shipment.objects.create(
                shipment_type_id = data.get('shipment_type_id'),
                shipping_address = data.get('shipping_address'),
                billing_address = data.get('billing_address'),
                product_price = product_price,
                delivery_cost=delivery_cost,
                final_price=float(product_price)+float(delivery_cost),
            )
            quantity = data.get('quantity')
            shipment_detail = ShipmentDetails.objects.create(
                shipment = shipment,
                product_id = data.get('product_id'),
                quantity = data.get('quantity'),
                price_per_unit = data.get('product_price'),
                price = float(shipment.final_price) *float(quantity),
            )
            status, created = StatusCatlog.objects.get_or_create(
                status_name='Order Placed'
            )
            shipment_status = ShipmentStatus.objects.create(
                shipment=shipment,
                status_catlog=status,
                notes='Order Placed'

            )    
            return Response({'status': 'success', 
                    'msg': 'User Created Successfully'})

    def delete(self, request, pk, format=None):
        obj = Shipment.objects.get(pk=pk)
        obj.delete()
        return Response({'status': 'success', 
                        'msg': 'Deleted Successfully'})


class ShipmentListAPIView(generics.ListAPIView):
    """ To get all shipment
    """
    permission_classes = (AllowAny,)
    serializer_class = ShipmentDetailSerializer
    # pagination_class = PagesPagination
    
    def get_queryset(self):
        return ShipmentDetails.objects.all()


class Predata(APIView):
    """ To get all products and shipment types
    """

    permission_classes = (AllowAny, )

    def get(self, request, format=None):
        try:
            product_obj = Products.objects.all()
            stype_obj = ShipmentType.objects.all()
            stype = ShipmentTypeSerializer(stype_obj, many=True)
            product = ProductsSerializer(product_obj, many=True)
            return Response({
                'status': 'success',
                'shipment_type': stype.data,
                'products': product.data
                })
        except ObjectDoesNotExist:
            return Response({'status': 'failed',
                            'error': 'Object does not exist'},
                            status=HTTP_400_BAD_REQUEST)