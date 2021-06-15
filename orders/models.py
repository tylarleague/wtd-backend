from django.db import models
from simple_history.models import HistoricalRecords
# Create your models here.
from accounts.models import ClientProfile, Person, ProviderProfile
from django.contrib.postgres.fields import JSONField
from datetime import datetime, timedelta
class Order(models.Model):
    owner = models.ForeignKey(
        ClientProfile, related_name="owner_related_orders", on_delete=models.CASCADE)
    patient = models.ForeignKey(
        Person, related_name="patient_related_orders", on_delete=models.CASCADE)
    from_location = JSONField(null=True, blank=True)
    to_location = JSONField(null=True, blank=True)
    order_date = models.DateField(null=True, blank=True)
    arrival_time = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=50, default="open")
    created_at = models.DateTimeField(auto_now_add=True)
    approved_by_client = models.BooleanField(default=False)
    # need_nurse = models.BooleanField(default=False)
    provider = models.ForeignKey(
        ProviderProfile, related_name="provider_related_orders", on_delete=models.CASCADE, null=True, blank=True)
    approved_by_provider = models.BooleanField(null=True, blank=True)
    notes = models.CharField(max_length=500, null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.id) + " related to user: " + str(self.owner.user.name) + " w/ phone #: " + str(self.owner.user.phone_number)

    @property
    def amb_arrival(self):
        # print('self.arrival_time', str(self.arrival_time))
        # print("teeest", datetime.strptime(str(self.arrival_time), "%H:%M:%S"))
        my_arrival_time = datetime.strptime(str(self.arrival_time), "%H:%M:%S")
        # print('SEEECONDS', self.order_related_invoice.duration_value)
        # print('mytest', my_arrival_time - timedelta(seconds=self.order_related_invoice.duration_value))

        return (my_arrival_time - timedelta(seconds=self.order_related_invoice.duration_value)).time()


class Invoice(models.Model):
    order = models.OneToOneField(
        Order, related_name="order_related_invoice", on_delete=models.CASCADE)
    distance_value = models.IntegerField()
    distance_text = models.CharField(max_length=50)
    duration_value = models.IntegerField()
    duration_text = models.CharField(max_length=50)
    cost = models.IntegerField()


    def __str__(self):
        return str(self.id) + " related to order: " + str(self.order.id)


class ExtraServices(models.Model):
    service_name = models.CharField(max_length=100)
    service_cost = models.IntegerField()
    # order = models.ManyToManyField(
    #     Order, related_name="ordr_extra_services", null=True, blank=True)

    def __str__(self):
        return str(self.id) + " - " + str(self.service_name )