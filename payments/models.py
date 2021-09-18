from django.db import models
from accounts.models import ClientProfile, Person, ProviderProfile, User
from orders.models import Order
# Create your models here.

class Payment(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_related_tokens", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="owner_related_tokens", on_delete=models.CASCADE)
    tap_token_id = models.CharField(max_length=500)
    tap_charge_id = models.CharField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return str(self.tap_token_id) + " related to order: " + str(self.order.id) + " for user " + str(self.user.phone_number)
