from django.db import models


class Order(models.Model):
    """Model representing an order."""

    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """String for representing the Model object."""

        return f'{self.id}'


class OrderDetail(models.Model):
    """Model representing an order detail."""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=False, blank=False)
    product = models.OneToOneField(
        'products.Product', on_delete=models.CASCADE, null=False, blank=False
    )
    quantity = models.IntegerField(default=0)

    class Meta:

        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'

    def __str__(self):
        """String for representing the Model object."""

        return f'{self.id}'

