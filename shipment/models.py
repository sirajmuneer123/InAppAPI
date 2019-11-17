from django.db import models

class ShipmentType(models.Model):
    """ Model to store shipment types
    """

    type_name = models.CharField(max_length=64)

    class Meta:
        default_permissions = ()
    def __str__(self):
        return self.type_name



class Shipment(models.Model):
    """ Model to store shipmets data
    """
    time_created = models.DateTimeField(auto_now_add=True)
    shipment_type = models.ForeignKey(ShipmentType,
                                on_delete=models.CASCADE)
    shipping_address = models.TextField()
    billing_address = models.TextField()
    product_price = models.DecimalField(decimal_places=2,
                                max_digits=8, default=0.0)
    delivery_cost = models.DecimalField(decimal_places=2,
                                max_digits=8, default=0.0)
    discount = models.DecimalField(decimal_places=2,
                                max_digits=8, default=0.0)
    final_price = models.DecimalField(decimal_places=2,
                                max_digits=8, default=0.0)

    class Meta:
        default_permissions = ()
    def __str__(self):
        return self.shipping_address

class Products(models.Model):
    """ Model to store shipment products
    """
    product_name = models.CharField(max_length=240)
    price = models.DecimalField(decimal_places=2, 
                            max_digits=8, default=0.0)
    delivery_cost = models.DecimalField(decimal_places=2, 
                            max_digits=8, default=0.0)

    class Meta:
        default_permissions = ()
    def __str__(self):
        return self.product_name


class ShipmentDetails(models.Model):
    """ Model to store shipment details
    """
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2,
                            max_digits=8, default=0.0)
    price_per_unit = models.DecimalField(decimal_places=2,
                            max_digits=8, default=0.0)
    price = models.DecimalField(decimal_places=2,
                            max_digits=8, default=0.0)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.product.product_name


class StatusCatlog(models.Model):
    """ Model to store status catlogs
    """
    status_name = models.CharField(max_length=255)

    class Meta:
        default_permissions = ()
    def __str__(self):
        return self.status_name


class ShipmentStatus(models.Model):
    """ Model to store shipment status
    """
    shipment = models.ForeignKey(Shipment, 
                                on_delete=models.CASCADE)
    status_catlog = models.ForeignKey(StatusCatlog, 
                                on_delete=models.CASCADE)
    status_time = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True)


    class Meta:
        default_permissions = ()
    
    def __str__(self):
        return self.status_catlog.status_name






